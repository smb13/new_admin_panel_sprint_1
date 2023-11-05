"""Main module to load data from  SQLite to Postgres."""
import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.db_settings import SQLITE_DB_PATH, dsl, tables_classes
from sqlite_to_postgres.logger import get_logger
from sqlite_to_postgres.pg_save import PostgresSaver
from sqlite_to_postgres.sl_extract import SQLiteExtractor

logger = get_logger('Load data')


@contextmanager
def connection_context_sqlite(db_path: str) -> sqlite3.Connection:
    """Configure connection to Sqlite DB.

    Args:
        db_path: Sqlite DB file path

    Yields:
        sqlite3.Connection: connection to Sqlite
    """
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    yield connection
    connection.close()


@contextmanager
def connection_context_pg(**kwargs) -> _connection:
    """Configure connection to sqlite DB.

    Args:
        kwargs: Postgres DB connection parameters

    Yields:
        _connection: connection to Postgres
    """
    connection = psycopg2.connect(**kwargs, cursor_factory=DictCursor)
    yield connection
    connection.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_connection: _connection) -> None:
    """Load data from  SQLite to Postgres.

    Args:
        connection: connection to Sqlite
        pg_connection: connection to Postgres
    """
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_connection)
    postgres_saver.truncate_tables(list(tables_classes.keys()))
    for table_name, table_class in tables_classes.items():
        data = sqlite_extractor.extract_data(table_name, table_class)
        postgres_saver.save_data(data, table_name)


if __name__ == '__main__':
    try:
        with connection_context_sqlite(SQLITE_DB_PATH) as sqlite_conn, connection_context_pg(**dsl) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
        logger.info('Process loading data from SQLite to Postgres databases finished successfully')
    except Exception as err:
        logger.error(f'Error during loading data from SQLite to Postgres databases: {err}')
