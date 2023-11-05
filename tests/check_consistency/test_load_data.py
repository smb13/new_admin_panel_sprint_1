from datetime import datetime

from sqlite_to_postgres.db_settings import (ROWS_IO_BUFFER, SCHEMA,
                                            SQLITE_DB_PATH, dsl,
                                            tables_classes)
from sqlite_to_postgres.load_data import (connection_context_pg,
                                          connection_context_sqlite,
                                          load_from_sqlite)


def test_load_from_sqlite():
    """Test for sqlite_to_postgres package."""
    with (connection_context_sqlite(SQLITE_DB_PATH) as sqlite_conn, connection_context_pg(**dsl) as pg_conn):
        load_from_sqlite(sqlite_conn, pg_conn)
        for table_name in tables_classes:

            # Check number of rows in corresponding tables of SQLite and Postgres DBs
            sqlite_cursor = sqlite_conn.cursor()
            pg_cursor = pg_conn.cursor()
            query_template = 'SELECT COUNT(*) FROM {table_name}'
            sqlite_cursor.execute(query_template.format(table_name=table_name))
            sqlite_rows_number = dict(sqlite_cursor.fetchone()).get('COUNT(*)')
            query_template = 'SELECT COUNT(*) FROM {schema}.{table_name}'
            pg_cursor.execute(query_template.format(schema=SCHEMA, table_name=table_name))
            pg_rows_number = dict(pg_cursor.fetchone()).get('count')
            assert sqlite_rows_number == pg_rows_number

            # Check field by field all records in corresponding tables of SQLite and Postgres DBs
            query_template = 'SELECT * FROM {table_name}'
            sqlite_cursor.execute(query_template.format(table_name=table_name))
            sqlite_data = []
            while True:
                result = sqlite_cursor.fetchmany(ROWS_IO_BUFFER)
                if len(result) == 0:
                    break
                for row in result:
                    sqlite_data.append(dict(row))
            for sqlite_row in sqlite_data:
                row_id = sqlite_row.get('id')
                query_template = "SELECT * FROM {schema}.{table_name} WHERE id='{row_id}'"
                pg_cursor.execute(query_template.format(schema=SCHEMA, table_name=table_name, row_id=row_id))
                pg_row = dict(pg_cursor.fetchone())
                for key in sqlite_row.keys():
                    if key in ('id', 'file_path'):
                        continue
                    if key == 'created_at':
                        sqlite_dt = datetime.strptime(sqlite_row.get(key) + ':00', "%Y-%m-%d %H:%M:%S.%f%z")
                        assert sqlite_dt == pg_row.get('created')
                        continue
                    if key == 'updated_at':
                        sqlite_dt = datetime.strptime(sqlite_row.get(key) + ':00', "%Y-%m-%d %H:%M:%S.%f%z")
                        assert sqlite_dt == pg_row.get('modified')
                        continue
                    assert sqlite_row.get(key) == pg_row.get(key)
