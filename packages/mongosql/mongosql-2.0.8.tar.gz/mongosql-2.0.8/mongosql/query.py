"""
### Creating a MongoQuery
`MongoQuery` is the main tool that lets you execute JSON Query Objects against an SqlAlchemy-handled database.

There are two ways to use it:

1. Construct `MongoQuery` manually, giving it your model:

    ```python
    from mongosql import MongoQuery
    from .models import User  # Your model

    ssn = Session()

    # Create a MongoQuery, using an initial Query (possibly, with some initial filtering applied)
    mq = MongoQuery(User).from_query(ssn.query(User))
    ```

2. Use the convenience mixin for your Base:

    ```python
    from sqlalchemy.ext.declarative import declarative_base
    from mongosql import MongoSqlBase

    Base = declarative_base(cls=(MongoSqlBase,))

    class User(Base):
        #...
    ```

    Using this Base, your models will have a shortcut method which returns a `MongoQuery`:

    ```python
    User.mongoquery(session)
    User.mongoquery(query)
    ```

    With `mongoquery()`, you can construct a query from a session:

    ```python
    mq = User.mongoquery(session)
    ```

    .. or from an [sqlalchemy.orm.Query](https://docs.sqlalchemy.org/en/latest/orm/query.html),
    which allows you to apply some initial filtering:

    ```python
    mq = User.mongoquery(
        session.query(User).filter_by(active=True)  # Only query active users
    )
    ```

### Reusable
A `MongoQuery` object itself is not reusable: it can make just one query.

However, it makes sense to save some initialization and keep it ready for new requests.
For performance reasons, this has to be done manually with the `Reusable` wrapper:

```python
mq_factory = Reusable(User.mongoquery(session))
```

The wrapped object has all the methods of a `MongoQuery`, but will make a proper copy when used.
Think of it as a factory.

### Querying: `MongoQuery.query()`
Once a `MongoQuery` is prepared, you can give it a QueryObject:

```python
# QueryObject
query_object = {
  'filter': {
    'sex': 'f',
    'age': { '$gte': 18, '$lte': 25 },  # 18..25 years
  },
  'order': ['weight+'],  #  slims first
  'limit': 50,  # just enough :)
}

# MongoQuery
mq = User.mongoquery(ssn).query(**query_object)
```

### Getting Results: `MongoQuery.end()`
Because `MongoQuery` is just a wrapper around an SqlAlchemy's `Query`, you can get that `Query`
and get results out of it:

```python
# By calling the `MongoQuery.end()` method, you get an SqlAlchemy `Query`:
q = mq.end()  # SqlALchemy Query

# Execute the query and fetch results
girls = q.all()
```

### Getting All Sorts of Results
Let's remember that the Query generated by MongoQuery can return three sorts of results:

1. Entities. When the API user has requested an entity of a list of them.
3. Integer. When the API user has used `{count: 1}`.
2. Tuples. This is what you get when the API user has used the [Aggregate Operation](#aggregate-operation).

`MongoQuery` has three methods that help you detect what you get:

1. `MongoQuery.result_contains_entities()`
2. `MongoQuery.result_is_scalar()`
3. `MongoQuery.result_is_tuples()`

Here's how to use it:

```python
def get_result(mq: MongoQuery, query: Query):
    # Handle: Query Object has count
    if mq.result_is_scalar():
        return {'count': query.scalar()}

    # Handle: Query Object has group_by and yields tuples
    if mq.result_is_tuples():
        # zip() column names together with the values, and make it into a dict
        return {
            'results': [dict(zip(row.keys(), row))
                        for row in query]
        }

    # Regular result: entities
    return {
        'users': query.all()
    }
```

Most likely, you won't need to handle that at all: just use  [CRUD Helpers](#crud-helpers)
that implement most of this logic for you.


"""

from copy import copy

from sqlalchemy import inspect, exc as sa_exc
from sqlalchemy.orm import Query, Load, defaultload

from mongosql import RuntimeQueryError, BaseMongoSqlException
from .bag import ModelPropertyBags
from . import handlers
from .exc import InvalidQueryError
from .util import MongoQuerySettingsHandler, CountingQuery

from typing import Union, Mapping, Iterable, Tuple, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import RelationshipProperty
from .util import MongoQuerySettingsDict


class MongoQuery:
    """ MongoQuery is a wrapper around SqlAlchemy's `Query` that can safely execute JSON Query Objects """

    # The class to use for getting structural data from a model
    _MODEL_PROPERTY_BAGS_CLS = ModelPropertyBags

    def __init__(self, model: DeclarativeMeta, handler_settings: Union[Mapping, MongoQuerySettingsDict, None] = None):
        """ Init a MongoDB-style query

        :param model: SqlAlchemy model to make a MongoSQL query for.
        :param handler_settings: Settings for Query Object handlers. See MongoQuerySettingsDict
        """
        # Aliases?
        if inspect(model).is_aliased_class:
            raise TypeError('MongoQuery does not accept aliases. '
                            'If you want to query an alias, do it like this: '
                            'MongoQuery(User).aliased(aliased(User))')

        # Init with the model
        self.model = model  # model, or its alias (when used with self.aliased())
        self.bags = self._MODEL_PROPERTY_BAGS_CLS.for_model(self.model)

        # Initialize the settings
        self.handler_settings = self._init_handler_settings(handler_settings or {})
        self._query_options = {
            # See: options()
            'no_limit_offset': False,
        }

        # Initialized later
        self._query = None  # type: Query | None
        self._parent_mongoquery = None  # type: MongoQuery | None
        self.input_value = None  # type: dict | None

        # Get ready: Query object handlers
        self._init_query_object_handlers()

        # Load interface join path
        # These are just the defaults ; as_relation() will override them when working with
        # deeper relationships
        self._join_path = ()
        self._as_relation = Load(self.model)

        # Cached MongoQuery objects for nested relationships
        self._nested_mongoqueries = dict()  # type: dict[str, MongoQuery]

        # NOTE: keep in mind that this object is copy()ed in order to make it reusable.
        # This means that every property that can't be safely reused has to be copy()ied manually
        # inside the __copy__() method.
        # A good example is the `_as_relation()` method: if not copied properly, subsequent queries
        # will inherit all option()s from the previous queries and lead to all sorts of weird effects!
        # So, whenever you add a property to this object, make sure you understand its copy() behavior.

    def __copy__(self) -> 'MongoQuery':
        """ MongoQuery can be reused: wrap it with Reusable() which performs the automatic copy()

            It actually makes sense to have reusable MongoQuery because there's plenty of settings
            you don't want to parse over ang over again.

            This method implements proper copying so that this MongoQuery can be reused.
        """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)

        # Copy Query Object handlers
        for name in self.HANDLER_ATTR_NAMES:
            setattr(result, name, copy(getattr(result, name)))

        # Copy mutable objects
        result._query_options = result._query_options.copy()

        # Re-initialize properties that can't be copied
        self.as_relation(None)  # reset the Load() interface. Outside code will have to set it up properly
        self._query = None

        return result

    def options(self, *, no_limit_offset=False):
        """ Set options for this query to alter its behavior

        Args:
            no_limit_offset: Disable putting LIMIT/OFFSET on the query.
                This is useful when you already have a MongoQuery configured but want to make
                an unrestricted query with the same settings.
                Note that this setting only has effect on the immediate query; it does not remove limits/offsets
                from nested queries (i.e. queries for related objects)
        """
        # Option: no limit offset
        assert isinstance(no_limit_offset, bool)
        self._query_options['no_limit_offset'] = no_limit_offset
        # Can apply immediately
        self.handler_limit.skip_this_handler = no_limit_offset

        return self

    def from_query(self, query: Query) -> 'MongoQuery':
        """ Specify a custom sqlalchemy query to work with.

        It can have, say, initial filtering already applied to it.
        It no default query is provided, _from_query() will use the default.

        :param query: Initial sqlalchemy query to work with (e.g. with initial filters pre-applied)
        :type query: sqlalchemy.orm.Query
        """
        self._query = query
        return self

    def with_session(self, ssn: Session) -> 'MongoQuery':
        """ Query with the given sqlalchemy Session

        Args:
            ssn: The SqlAlchemy `Session` to use for querying
        """
        self._query = self._from_query().with_session(ssn)
        return self

    def as_relation(self, join_path: Union[Tuple[RelationshipProperty], None] = None):
        """ Handle a model in relationship with another model

            This internal method is used when working with deeper relations.
            For example, when you're querying `User`, who has `User.articles`, and you want to specify lazyload() on
            the fields of that article, you can't just do `lazyload(User.articles)` ; you have to tell sqlalchemy that
            you actually mean a model that is going to be loaded through a relationship.
            You do it this way:

                defaultload(models.User.articles).lazyload(models.Article)

            Then SqlAlchemy will know that you actually mean a related model.

            To achieve this, we keep track of nested relations in the form of `join_path`.
            `self._as_relation` is the Load() interface for chaining methods for deeper relationships.

            :param join_path: A tuple of relationships leading to this query.
        """
        if join_path:
            self._join_path = join_path
            self._as_relation = defaultload(*self._join_path)
        else:
            # Set default
            # This behavior is used by the __copy__() method to reset the attribute
            self._join_path = ()
            self._as_relation = Load(self.model)
        return self

    def as_relation_of(self, mongoquery: 'MongoQuery', relationship: RelationshipProperty) -> 'MongoQuery':
        """ Handle the query as a sub-query handling a relationship

        This is used by the MongoJoin handler to build queries to related models.

        :param mongoquery: The parent query
        :param relationship: The relationship
        """
        return self.as_relation(mongoquery._join_path + (relationship,))

    def aliased(self, model: DeclarativeMeta) -> 'MongoQuery':
        """ Make a query to an aliased model instead.

        This is used by MongoJoin handler to issue subqueries.
        Note that the method modifies the current object and does not make a copy!

        Note: should always be called after as_relation_of(), not before!

        :param model: Aliased model
        """
        # Aliased bags
        self.bags = self.bags.aliased(model)
        self.model = model

        # Aliased loader interface
        # Currently, our join path looks like this: [..., User]
        # Now, when we're using an alias instead, we have to replace that last element with an alias too
        # SqlAlchemy 1.2.x used to work well without doing it;
        # SqlAlchemy 1.3.x now requires adapting a relationship by using of_type() on it.
        # See: https://github.com/sqlalchemy/sqlalchemy/issues/4566
        if self._join_path:  # not empty
            # Okay. First. Replace the last element on the join path with the aliased model's relationship
            new_join_path = self._join_path[0:-1] + (self._join_path[-1].of_type(model),)
            # Second. Apply the new join path
            self.as_relation(new_join_path)
        else:  # empty
            self._as_relation = Load(self.model)  # use the alias

        # Aliased handlers
        for handler_name in self.HANDLER_ATTR_NAMES:
            setattr(self, handler_name,
                    getattr(self, handler_name).aliased(model))

        return self

    def query(self, **query_object: Any) -> 'MongoQuery':
        """ Build a MongoSql query from an object

        :param query_object: The Query Object to execute.
        :raises InvalidQueryError: unknown Query Object operations provided (extra keys)
        :raises InvalidQueryError: syntax error for any of the Query Object sections
        :raises InvalidColumnError: Invalid column name provided in the input
        :raises InvalidRelationError: Invalid relationship name provided in the input
        :rtype: MongoQuery
        """
        # Prepare Query Object
        for handler_name, handler in self._handlers():
            query_object = handler.input_prepare_query_object(query_object)

        # Check if Query Object keys are all right
        invalid_keys = set(query_object.keys()) - self.HANDLER_NAMES
        if invalid_keys:
            raise InvalidQueryError('Unknown Query Object operations: {}'.format(', '.join(invalid_keys)))

        # Store
        self.input_value = query_object

        # Bind every handler with ourselves
        # We do it as a separate step because some handlers want other handlers in a pristine condition.
        # Namely, MongoAggregate wants to copy MongoFilter before it receives any input.
        for handler_name, handler in self._handlers():
            handler.with_mongoquery(self)

        # Process every field with its method
        # Every handler should be invoked because they may have defaults even when no input was provided
        for handler_name, handler in self._handlers_ordered_for_query_method():
            # Query Object value for this handler
            input_value = query_object.get(handler_name, None)

            # Disabled handlers exception
            # But only test that if there actually was any input
            if input_value is not None:
                self._raise_if_handler_is_not_enabled(handler_name)

            # Use the handler
            # Run it even when it does not have any input
            handler.input(input_value)

        # Done
        return self

    def end(self) -> Query:
        """ Get the resulting sqlalchemy `Query` object """
        # The query
        q = self._from_query()

        # Apply every handler
        for handler_name, handler in self._handlers_ordered_for_end_method():
            if not handler.skip_this_handler:
                # Apply the handler
                try:
                    q = handler.alter_query(q, as_relation=self._as_relation)
                # Enrich SqlAlchemy errors with MongoSQL context (because it's very difficult to debug its cryptic messages)
                except sa_exc.SQLAlchemyError as e:
                    # Get model name by backtracing MongoQuery objects
                    model_name = []
                    mq = self
                    while mq is not None:
                        model_name.append(mq.bags.model_name)
                        mq = mq._parent_mongoquery
                    model_name = ' -> '.join(reversed(model_name))

                    # Finally, raise one rich error
                    raise RuntimeQueryError(f'Error processing MongoQuery({model_name}).{handler_name}: {e}') from e

        return q

    def end_count(self) -> CountingQuery:
        """ Get the result, and also count the total number of rows.

            Be aware that the cost will be substantially higher than without the total number,
            but still cheaper than two separate queries.

            Numbers: this gives about 50% boost to small result sets, and about 15% boost to larger result sets.

            See [CountingQuery](#countingqueryquery) for more details.

            Example:

                ```python
                q = User.mongoquery(ssn).query(...).end_count()

                # Get the count
                q.count  # -> 127

                # Get results
                list(q)  # -> [User, ...]

                # (!) only one actual SQL query was made
                ```
        """
        # Get the query and wrap it with a counting query
        return CountingQuery(self.end())

    # Extra features

    def result_contains_entities(self) -> bool:
        """ Test whether the result will contain entities.

        This is normally the case in the absence of 'aggregate', 'group', and 'count' queries.
        """
        return self.handler_aggregate.is_input_empty() and \
               self.handler_group.is_input_empty() and \
               self.handler_count.is_input_empty()

    def result_is_scalar(self) -> bool:
        """ Test whether the result is a scalar value, like with count

            In this case, you'll fetch it like this:

                MongoQuery(...).end().scalar()
        """
        return not self.handler_count.is_input_empty()

    def result_is_tuples(self) -> bool:
        """ Test whether the result is a list of keyed tuples, like with group_by

            In this case, you might fetch it like this:

                res = MongoQuery(...).end()
                return [dict(zip(row.keys(), row)) for row in res], None
        """
        return not self.handler_aggregate.is_input_empty() or \
               not self.handler_group.is_input_empty()

    def ensure_loaded(self, *cols: Iterable[str]) -> 'MongoQuery':
        """ Ensure the given columns, relationships, and related columns are loaded

            Despite any projections and joins the user may be doing, make sure that the given `cols` are loaded.
            This will ensure that every column is loaded, every relationship is joined, and none of those is included
            into `projection` and `pluck_instance`.

            This method is to be used by the application code to handle the following situation:
            * The API user has requested only fields 'a', 'b', 'c' to be loaded
            * The application code needs field 'd' for its operation
            * The user does not want to see no 'd' in the output.
            Solution: use ensure_loaded('d'), and then pluck_instance()

            Limitations:

            1. If the user has requested filtering on a relationship, you can't use ensure_loaded() on it.
                This method will raise an InvalidQueryError().
                This makes sense, because if your application code relies on the presence of a certain relationship,
                it certainly needs it fully loaded, and unfiltered.
            2. If the request contains no entities (e.g. 'group' or 'aggregate' handlers are used),
               this method would throw an AssertionError

            If all you need is just to know whether something is loaded or not, use MongoQuery.__contains__() instead.

            Remember that every time you use ensure_loaded() on a relationship, you disable the possibility of filtering for it!

            :param cols: Column names ('age'), Relation names ('articles'), or Related column names ('articles.name')
            :raises InvalidQueryError: cannot merge because the relationship has a filter on it
            :raises ValueError: invalid column or relationship name given.
                It does not throw `InvalidColumnError` because that's likely your error, not an error of the API user :)
        """
        assert self.result_contains_entities(), 'Cannot use ensure_loaded() on a result set that does not contain entities'

        # Tell columns and relationships apart
        columns = []
        relations = {}
        for name in cols:
            # Tell apart
            if name in self.bags.related_columns:
                # A related column will initialize a projection
                relation_name, column_name = name.split('.', 1)
                relations.setdefault(relation_name, {})
                relations[relation_name].setdefault('project', {})
                relations[relation_name]['project'][column_name] = 1
            elif name in self.bags.relations:
                # A relation will init an empty object
                relations.setdefault(name, {})
            elif name in self.bags.columns:
                # A column will just be loaded
                columns.append(name)
            else:
                raise ValueError('Invalid column or relation name given to ensure_loaded(): {!r}'
                                 .format(name))

        # Load all them
        try:
            self.handler_project.merge(columns, quietly=True, strict=True)
            self.handler_join.merge(relations, quietly=True, strict=True)
        except InvalidQueryError as e:
            raise InvalidQueryError('Failed to process ensure_loaded({}): {}'.format(cols, str(e))) from e

        # Done
        return self

    def get_final_query_object(self) -> dict:
        """ Get the final Query Object dict (after all handlers have applied their defaults).

        This Query Object will contain the name of every single handler, including those that were not given any input.
        """
        ret = {
            name: handler.get_final_input_value()
            for name, handler in self._handlers()
        }

        # Fix limit: keys 'skip' and 'limit'
        ret.update(ret['limit'])

        # Done
        return ret

    def get_projection_tree(self) -> dict:
        """ Get a projection-like dict that maps every included column to 1,
            and every relationship to a nested projection dict.

            Example:

                ```python
                MongoQuery(User).query(join={'articles': dict(project=('id',))}).handler_join.projection
                #-> {'articles': {'id': 1}}
                ```

                This is mainly useful for debugging nested Query Objects.
            Returns:
                dict: the projection
        """
        ret = {}
        ret.update(self.handler_project.projection)
        ret.update(self.handler_join.get_projection_tree())
        ret.update(self.handler_joinf.get_projection_tree())
        return ret

    def get_full_projection_tree(self) -> dict:
        """ Get a full projection tree that mentions every column, but only those relationships that are loaded
            :rtype: dict
        """
        ret = {}
        ret.update(self.handler_project.get_full_projection())
        ret.update(self.handler_join.get_full_projection_tree())
        ret.update(self.handler_joinf.get_full_projection_tree())
        return ret

    def pluck_instance(self, instance: object) -> dict:
        """ Pluck an sqlalchemy instance and make it into a dict

            This method should be used to prepare an object for JSON encoding.
            This makes sure that only the properties explicitly requested by the user get included
            into the result, and *not* the properties that your code may have loaded.

            Projection and Join properties are considered.

            :param instance: object
            :rtype: dict
        """
        if not isinstance(instance, self.bags.model):  # bags.model, because self.model may be aliased
            raise ValueError('This MongoQuery.pluck_instance() expects {}, but {} was given'
                             .format(self.bags.model, type(instance)))
        # First, projection will do what it wants.
        # By the way, it will also generate a dictionary
        dct = self.handler_project.pluck_instance(instance)
        # Now, the joins will add more fields
        dct.update(self.handler_join.pluck_instance(instance))
        dct.update(self.handler_joinf.pluck_instance(instance))
        # Seems like there's no one else?
        # Done.
        return dct

    def __contains__(self, key: str) -> bool:
        """ Test if a property is going to be loaded by this query """
        return key in self.handler_project or key in self.handler_join

    def __repr__(self):
        return 'MongoQuery({})'.format(str(self.model))

    # region Query Object handlers

    # This section initializes every Query Object handler, one per method.
    # Doing it this way enables you to override the way they are initialized, and use a custom query class with
    # custom settings.

    _QO_HANDLER_PROJECT = handlers.MongoProject
    _QO_HANDLER_SORT = handlers.MongoSort
    _QO_HANDLER_GROUP = handlers.MongoGroup
    _QO_HANDLER_JOIN = handlers.MongoJoin
    _QO_HANDLER_JOINF = handlers.MongoFilteringJoin
    _QO_HANDLER_FILTER = handlers.MongoFilter
    _QO_HANDLER_AGGREGATE = handlers.MongoAggregate  # Use MongoAggregateInsecure for backwards compatibility
    _QO_HANDLER_LIMIT = handlers.MongoLimit
    _QO_HANDLER_COUNT = handlers.MongoCount

    HANDLER_NAMES = frozenset(('project',
                               'sort',
                               'group',
                               'join',
                               'joinf',
                               'filter',
                               'aggregate',
                               'limit',
                               'count'))
    HANDLER_ATTR_NAMES = frozenset('handler_'+name
                                   for name in HANDLER_NAMES)

    def _handlers(self):
        """ Get the list of all (handler_name, handler) """
        return (
            # Note that the ordering of these handlers may actually influence the way queries are processed!

            # Considerations for the input() method:
            # 1. 'project' before 'join'
            #    Because 'project' will try to send relationships to the 'join' handler,
            #    and MongoJoin has to have input() already called by then.
            #    NOTE: this is the only handler that has preferences for its input() method.
            #          Because other handlers do not care, and this one does, the best way to bring it down
            #          to the bottom is to use reversed(self._handlers()).
            #
            # Considerations for the alter_query() method:
            # 1. 'limit' after 'order_by':
            #    'order_by' does not like limits
            # 2. 'join' after 'filter' and 'limit'
            #    Because 'join' handler may make it into a subquery,
            #    and at that point is has to have all filters and limits applied
            # 3. 'aggregate' before 'sort', 'group', 'filter'
            #    Because aggregate handler uses Query.select_from(), which can only be applied to a query
            #    without any clauses like WHERE, ORDER BY, GROUP BY
            # 4. 'sort' before 'join'
            #    Because join makes a subquery, and it has to contain ordering within it.
            # 5. 'limit' after everything
            #    Because it will wrap everything into a subquery, which has a different name.
            #    However, 'join' and 'joinf' somehow manage to handle the situation, so the requirement is restated:
            #    "after everything", but can be before "join".
            # *. There may be others that the author is not aware of... yet.
            ('project', self.handler_project),
            ('aggregate', self.handler_aggregate),
            ('sort', self.handler_sort),
            ('group', self.handler_group),
            ('filter', self.handler_filter),
            ('limit', self.handler_limit),
            ('join', self.handler_join),
            ('joinf', self.handler_joinf),
            ('count', self.handler_count)
        )

    def _handlers_ordered_for_query_method(self):
        """ Handlers in an order suitable for the query() method """
        # reversed() is applied as a hack to move 'project' below 'join'.
        return reversed(self._handlers())

    def _handlers_ordered_for_end_method(self):
        """ Handlers in an order suitable for the end() method """
        return self._handlers()

    # for IDE completion
    handler_project = None  # type: handlers.MongoProject
    handler_sort = None  # type: handlers.MongoSort
    handler_group = None  # type: handlers.MongoGroup
    handler_join = None  # type: handlers.MongoJoin
    handler_joinf = None  # type: handlers.MongoJoinf
    handler_filter = None  # type: handlers.MongoFilter
    handler_aggregate = None  # type: handlers.MongoAggregate
    handler_limit = None  # type: handlers.MongoLimit
    handler_count = None  # type: handlers.MongoCount

    def _init_query_object_handlers(self):
        """ Initialize every Query Object handler """
        for name in self.HANDLER_NAMES:
            # Every handler: name, attr, clas
            handler_attr_name = 'handler_' + name
            handler_cls_attr_name = '_QO_HANDLER_' + name.upper()
            handler_cls = getattr(self, handler_cls_attr_name)

            # Use _init_handler()
            setattr(self, handler_attr_name,
                    self._init_handler(name, handler_cls)
                    )

        # Check settings
        self.handler_settings.raise_if_invalid_handler_settings(self)

    def _init_handler(self, handler_name: str, handler_cls: type):
        """ Init a handler, and load its settings """
        handler_settings = self.handler_settings.get_settings(handler_name, handler_cls)
        return handler_cls(self.model, self.bags, **handler_settings)

    # endregion

    # region Internals

    def _init_handler_settings(self, handler_settings: Mapping) -> MongoQuerySettingsHandler:
        """ Initialize: handler settings """
        # A special case for 'join'
        if handler_settings.get('join_enabled', True) is False:
            # If 'join' is explicitly disabled, disable 'joinf' as well
            # This is for security so that one doesn't forget to disable them both.
            handler_settings['joinf_enabled'] = False

        # A special case for 'raiseload'
        if handler_settings.pop('raiseload', False):
            # Can't combine
            assert 'raiseload_col' not in handler_settings
            assert 'raiseload_rel' not in handler_settings
            # Both True
            handler_settings['raiseload_col'] = True
            handler_settings['raiseload_rel'] = True

        # Create the object
        hso = MongoQuerySettingsHandler(handler_settings)
        hso.validate_related_settings(self.bags)

        # Done
        return hso

    def _from_query(self) -> Query:
        """ Get the query to work with, or initialize one

            When the time comes to build an actual SqlAlchemy query, we're going to use the query that the user has
            provided with from_query(). If none was provided, we'll use the default one.
        """
        return self._query or Query([self.model])

    def _init_mongoquery_for_related_model(self, relationship_name: str) -> 'MongoQuery':
        """ Create a MongoQuery object for a model, related through a relationship with the given name.

            This method configures queries made on related models.
            Note that this method is only called once for every relationship.

            See: _get_nested_mongoquery() for more info
        """
        # Get the relationship
        # There must be no exceptions here, because JoinHandler is the only guy using this method,
        # and it should already have validated relationship name.
        # Meaning, we can be pretty sure `relationship_name` exists
        target_model = self.bags.relations.get_target_model(relationship_name)

        # Make a new MongoQuery
        handler_settings = self.handler_settings.settings_for_nested_mongoquery(relationship_name, target_model)
        mongoquery = self.__class__(target_model, handler_settings)

        # Done
        return mongoquery

    def _get_nested_mongoquery(self, relationship_name: str) -> 'MongoQuery':
        """ Get a MongoQuery for a nested model (through a relationship)

        Remember that the 'join' operation support nested queries!
        And those queries also support projections, filters, joins, and whatnot.
        This method will correctly load nested configuration from self.handler_settings,
        which enables you to set up your security and preferences for queries on related models.

        Example:

        mq = MongoQuery(Comment, dict(
            allowed_relations=('author',),  # only allow one relationship to be joined
            related={
                'author': dict(  # settings for queries on this relationship
                    join=False,  # disable further joins
                    force_exclude=('password',)  # can't get it
                )
            }
        ))

        In this case, the API user won't be able to get the password by join()ing to it from other entities.

        Note that this method does not call as_relation() nor aliased().
        You'll have to do it yourself.
        """
        # If there's no nested MongoQuery inited, make one
        if relationship_name not in self._nested_mongoqueries:
            self._nested_mongoqueries[relationship_name] = self._init_mongoquery_for_related_model(relationship_name)

        # Get a cached nested MongoQuery
        nested_mq = self._nested_mongoqueries[relationship_name]

        # Make a copy, set as_relation() properly, put an alias on it
        nested_mq = copy(nested_mq)

        # Parent relationship to self
        nested_mq._parent_mongoquery = self

        # Done
        return nested_mq

    def _raise_if_handler_is_not_enabled(self, handler_name: str):
        """ Raise an error if a handler is not enabled.

            This is used by:
            * query() method, to raise errors when a user provides input to a disabled handler
            * MongoProject.input() method, which feeds MongoJoin with projections, and has to check settings

            :return:
        """
        self.handler_settings.raise_if_not_handler_enabled(self.bags.model_name, handler_name)

    # endregion
