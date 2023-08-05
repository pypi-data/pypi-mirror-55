#!/usr/bin/env python
# coding: utf-8

import ibm_db

from myorm.dbobject import DbObject
from myorm.fields import ForeignKey


class IsNull:
    """ Used as identifier for NULL values in query_args """

    def __init__(self):
        pass


class Db2Adaptor(object):

    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_connection(self):
        connection = ibm_db.connect(self.connection_string, "", "")
        return connection

    def execute_query(self, query, query_args):
        connection = self.get_connection()
        stmt = ibm_db.prepare(connection, query)
        if not query_args:
            ibm_db.execute(stmt)
        else:
            query_args = [q for q in query_args if not isinstance(q, IsNull)]
            for idx, arg in enumerate(query_args):
                ibm_db.bind_param(stmt, idx, arg)
            ibm_db.execute(stmt)
        result = []
        tuple_ = ibm_db.fetch_tuple(stmt)
        while tuple_ is not False:
            result.append(tuple[0])
        connection = self.get_connection()
        lst_stm = ibm_db.prepare(connection, "SELECT IDENTITY_VAL_LOCAL() AS VAL FROM SYSIBM.SYSDUMMY1")
        ibm_db.execute(lst_stm)
        last_id = ibm_db.fetch_tuple(lst_stm)
        return (result, last_id)

    def get_filter_query(self, filter_partial):
        key, value = list(filter_partial.items())[0]
        if key.endswith('__in'):
            query = ('%s IN (%s)' % (key.replace('__in', ''), ', '.join('?' * len(value))))
        elif key.endswith('__lt'):
            query = '%s < %s' % (key.replace('__lt', ''), '?')
        elif key.endswith('__lte'):
            query = '%s <= %s' % (key.replace('__lte', ''), '?')
        elif key.endswith('__gt'):
            query = '%s > %s' % (key.replace('__gt', ''), '?')
        elif key.endswith('__gte'):
            query = '%s >= %s' % (key.replace('__gte', ''), '?')
        else:
            if value is not None:
                query = '%s=?' % key
            else:
                query = '%s IS NULL' % key
                value = IsNull()
        return query, value

    def get_exclude_query(self, exclude_partial):
        key, value = list(exclude_partial.items())[0]
        if key.endswith('__in'):
            query = ('%s NOT IN (%s)' % (key.replace('__in', ''), ', '.join('?' * len(value))))
        elif key.endswith('__lt'):
            query = '%s >= %s' % (key.replace('__lt', ''), '?')
        elif key.endswith('__lte'):
            query = '%s > %s' % (key.replace('__lte', ''), '?')
        elif key.endswith('__gt'):
            query = '%s <= %s' % (key.replace('__gt', ''), '?')
        elif key.endswith('__gte'):
            query = '%s < %s' % (key.replace('__gte', ''), '?')
        else:
            if value is not None:
                query = '%s <> ?' % key
            else:
                value = IsNull()
                query = '%s IS NOT NULL' % key
        return query, value

    def get_select_query(self, base, *args, **kwargs):
        query = "SELECT %s FROM %s" % (', '.join(base.fieldnames), base.tablename)
        return query

    def get_insert_query(self, base, create_partial):
        values = []
        for field in base.fields:
            value = create_partial.get(field.fieldname)
            if isinstance(value, DbObject):
                value = value.id
            if value is None:
                try:
                    value = field.default
                except AttributeError:
                    pass
            values.append(value)
        query = "INSERT INTO %s (%s) VALUES (%s)" % (base.tablename,
                                                     ', '.join(base.fieldnames),
                                                     ', '.join(['?' for item in base.fields]))
        return (query, tuple(values))

    def get_delete_query(self, base):
        query = "DELETE FROM %s " % base.tablename
        return query

    def get_update_query(self, base, update_partial):
        values = []
        affected_fields = []
        settings = ''
        for field in base.fields:
            value = update_partial.get(field.fieldname)
            if not value:
                pass
            else:
                values.append(value)
                affected_fields.append(field.fieldname)

        settings = ', '.join(['%s=?' % item for item in affected_fields])
        query = "UPDATE %s SET %s " % (base.tablename, settings)
        return (query, tuple(values))

    def bulk_create(self, objects, base):
        max_params = 999
        max_inserts_per_query = int(max_params / len(base.fieldnames))
        iterations = (len(base.fieldnames) * len(objects)) / max_params

        lower = 0
        for i in range(0, int(iterations) + 1):
            lower = int(i * max_inserts_per_query)
            upper = int(lower + max_inserts_per_query)
            query, query_args = self.get_bulk_insert_query(objects[lower:upper], base)
            self.execute_query(query, query_args)

    def get_bulk_insert_query(self, objects, base):
        values = [tuple(getattr(item, fieldname) for fieldname in item.fieldnames) for item in objects]
        placeholders = ', '.join(['(%s)' % (', '.join("?" * len(item))) for item in values])
        query = '''INSERT INTO "%s" (%s) VALUES %s''' % (base.tablename, ', '.join(base.fieldnames), placeholders)
        return (query, tuple(v for tupl in values for v in tupl))

    def get_create_table_query(self, base, tablename):
        if not tablename:
            tablename = base.tablename
        query = "CREATE TABLE %s (%%s);" % tablename
        fk_fields = []
        fields = []
        fieldnames = []
        for field in base.fields:
            if isinstance(field, ForeignKey):
                fk_fields.append(field)
            fields.append(field)
            fieldnames.append(field.fieldname)

        field_queries = [field.partial_create_table_query for field in fields]

        for field in fk_fields:
            fieldnames.append(field.fieldname)
        field_queries.extend([field.partial_create_table_query_extension for field in fk_fields])

        query = query % ', '.join(field_queries)
        query = query % tuple(fieldnames)
        return (query, None)

    def get_drop_table_query(self, base, tablename):
        if not tablename:
            tablename = base.tablename
        query = "DROP TABLE %s;" % tablename
        return (query, None)

    def get_pkfield_create_query(self):
        return '%s INTEGER not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), PRIMARY KEY (id)'

    def get_integer_field_create_query(self):
        query = '%s INTEGER'
        if default is not None:
            query += ' DEFAULT %s' % default
        return query

    def get_char_field_create_query(self, field):
        return '%%s CHAR(%s)' % field.max_length

    def get_text_field_create_query(self):
        return '%s TEXT'

    def get_datetime_field_create_query(self, default):
        if default is None:
            default = 'NULL'
        elif default == 'now':
            default = 'CURRENT_TIMESTAMP'
        return '%%s TIMESTAMP DEFAULT %s' % default

    def get_boolean_field_create_query(self, default):
        return '%%s TINYINT DEFAULT %s' % default

    def get_foreignkey_field_create_query_base(self):
        return '%s INTEGER'

    def get_foreignkey_field_create_query_extension(self, reference):
        if type(DbObject) == type(reference):
            reference = reference.tablename
        return 'FOREIGN KEY(%%s) REFERENCES %s(id)' % (reference)

    def create_migration_table(self):
        query = """CREATE TABLE myorm_migrations(
                    name VARCHAR(250),
                    id INTEGER not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), PRIMARY KEY (id))"""
        try:
            self.execute_query(query, None)
        except:
            pass

    def get_done_migrations(self):
        query = "SELECT id, name FROM myorm_migrations"
        return self.execute_query(query, None)

    def insert_migration(self, name):
        query = "INSERT INTO myorm_migrations (name) VALUES (?)"
        return self.execute_query(query, (name,))
