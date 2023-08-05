import logging

from django.db.models.query import RawQuerySet

from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditManager, AuditQuerySet

logger = logging.getLogger(__name__)


# class WhereClause:
#     where_clause = []
#
#     def exists(self, item):
#         return self.where_clause.count(item) > 0
#
#     def add_connector(self, connector: str) -> None:
#         if not self.exists('WHERE'):
#             self.where_clause.append(f'WHERE')
#             self.where_clause.append(f' ')
#         else:
#             self.where_clause.append(f'{connector.upper()}')
#             self.where_clause.append(f' ')
#
#     def add_open_brace(self) -> bool:
#         if self.exists('WHERE'):
#             if len(self.where_clause) == 0 or self.where_clause[len(self.where_clause) - 1] != '(':
#                 self.where_clause.append('(')
#                 return True
#         return False
#
#     def add_close_brace(self) -> None:
#         self.where_clause.append(')')
#
#     def add(self, item) -> None:
#         if not self.exists(item):
#             self.where_clause.append(item)
#
#     def extend(self, itegrator):
#         if isinstance(itegrator, list):
#             for item in itegrator:
#                 self.add(item)
#
#     def getClauseStr(self):
#         return ''.join(self.where_clause)


class TreeAuditModelQuerySet(AuditQuerySet):
    def get_descendants(self, id=None, start=None, end=None, child_id='child_id', parent_id='parent_id', include_self=True) -> RawQuerySet:
        db_name = self.model._meta.db_table

        if isinstance(id, int):
            id = tuple([id])
        elif not isinstance(id, tuple):
            raise Exception(f'id must be list or int')

        res = super().raw(f'''WITH RECURSIVE r AS (
                            SELECT *, 1 AS level
                            FROM {db_name}
                            WHERE {child_id if include_self else parent_id} IN %s

                            union all

                            SELECT {db_name}.*, r.level + 1 AS level
                            FROM {db_name}
                                JOIN r
                            ON {db_name}.{parent_id} = r.{child_id})

                        select r.* from r limit %s offset %s
                        ''', params = (tuple(id), end, start))

        return res

    def get_descendants_count(self, id='id', limit=None, child_id='child_id', parent_id='parent_id', include_self=True) -> int:
        return len(self.get_descendants(id=id, end=limit, child_id=child_id, parent_id=parent_id, include_self=include_self))

    # def connection(self, children: List[Q], connector: str) -> List[str]:
    #     if isinstance(children, list):
    #         for child in children:
    #             if isinstance(child, Q):
    #                 if len(child.children) > 0:
    #                     open_brace = self.where_clause.add_open_brace()
    #                     self.where_clause.extend(self.connection(children=child.children, connector=child.connector))
    #                     if open_brace:
    #                         self.where_clause.add_close_brace()
    #             elif isinstance(child, tuple):
    #                 field_operator, value = child
    #                 items = field_operator.split('__')
    #                 operator = items[len(items) - 1]
    #                 field = '__'.join(items[0:len(items) - 1])
    #                 if operator == 'icontains':
    #                     self.where_clause.add_connector(connector)
    #                     self.where_clause.add_open_brace()
    #                     self.where_clause.where_clause.append(f"UPPER({field}) LIKE UPPER('%{value}%')")
    #                     self.where_clause.add_close_brace()
    #                 elif operator == 'exact':
    #                     self.where_clause.add_connector(connector)
    #                     self.where_clause.add_open_brace()
    #                     if value == None:
    #                         self.where_clause.where_clause.append(f"{field} IS NULL")
    #                     else:
    #                         self.where_clause.where_clause.append(f"{field} = {value}")
    #                     self.where_clause.add_close_brace()
    #                 else:
    #                     raise Exception(f'Unexcepted operator {operator}')
    #     else:
    #         logger.debug(f'children: {children}')

    # def _get_range_rows(self, *args, **kwargs):
    #     json = kwargs.get('json')
    #     distinct_field_names = kwargs.get('distinct_field_names')
    #     end = kwargs.get('end')
    #     start = kwargs.get('start')
    #
    #     criteria = self.get_criteria(json=json)
    #     self.where_clause = WhereClause()
    #     where_str = None
    #     if isinstance(criteria, Q) and isinstance(criteria.children, list) and len(criteria.children) > 0:
    #         self.connection(children=criteria.children, connector=criteria.connector)
    #         where_str = self.where_clause.getClauseStr()
    #
    #     sortClause = getAttr(json, "sortBy", [])
    #
    #     res = self.get_descendants(where_clause=where_str)
    #     return res

    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class TreeAuditModelManager(AuditManager):
    def get_range_rows1(self, request, function=None, distinct_field_names=None):
        request = DSRequest(request=request)
        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_queryset().get_range_rows(start=request.startRow, end=request.endRow, function=function, distinct_field_names=distinct_field_names, json=request.json)
        return res

    def get_descendants(self, id=None, limit=None, child_id='child_id', parent_id='parent_id', include_self=True) -> RawQuerySet:
        return self.get_queryset().get_descendants(id=id, end=limit, child_id=child_id, parent_id=parent_id, include_self=include_self)

    def get_descendants_count(self, id='id', limit=None, child_id='child_id', parent_id='parent_id', include_self=True) -> int:
        return self.get_queryset().get_descendants_count(id=id, limit=limit, child_id=child_id, parent_id=parent_id, include_self=include_self)

    def get_queryset(self):
        return TreeAuditModelQuerySet(self.model, using=self._db)
