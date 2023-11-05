"""Module processes saving data to Postgres DB."""
from dataclasses import astuple, fields

from sqlite_to_postgres.db_settings import ROWS_IO_BUFFER, SCHEMA
from sqlite_to_postgres.logger import get_logger


class PostgresSaver:
    """Class for save data to Postgres."""

    def __init__(self, connection):
        """Initialise PostgresSaver object.

        Args:
            connection: connection to Postgres DB
        """
        self.connection = connection
        self.logger = get_logger('PostgresSaver')

    def save_data(self, data: list, table_name: str) -> None:
        """Load data to Postgres DB.

        Args:
            data: data to load
            table_name: table name to load
        """
        try:
            cursor = self.connection.cursor()
            if len(data) > 0:
                first_row = data[0]
                column_names_list = [field.name for field in fields(first_row)]
                column_names = ','.join(column_names_list)
                col_count = ', '.join(['%s'] * len(column_names_list))
                while len(data) > 0:
                    values = []
                    for _i in range(ROWS_IO_BUFFER):
                        if len(data) > 0:
                            data_row = data.pop()
                            bind_values = cursor.mogrify(f'({col_count})', astuple(data_row)).decode('utf-8')
                            values.append(bind_values)
                        else:
                            break
                    values_str = ','.join(values)
                    query_template = 'INSERT INTO {schema}.{table_name} ({column_names}) VALUES {values_str}'
                    cursor.execute(query_template.format(schema=SCHEMA, table_name=table_name,
                                                         column_names=column_names, values_str=values_str))
                    cursor.execute('COMMIT')
            self.logger.info(f'Inserting into Postgres {SCHEMA}.{table_name} database finished successfully')
        except Exception as err:
            self.logger.error(f'Error during inserting into Postgres {SCHEMA}.{table_name} database: {err}')

    def truncate_tables(self, tables_names: list):
        """Truncate Postgres DB tables for loading.

        Args:
            tables_names: tables names to truncate
        """
        for table_name in tables_names:
            try:
                cursor = self.connection.cursor()
                cursor.execute(f'TRUNCATE content.{table_name} CASCADE')
                cursor.execute('COMMIT')
                self.logger.info(f'Truncating Postgres content.{table_name} database finished successfully')
            except Exception as err:
                self.logger.error(f'Error during truncating Postgres content.{table_name} database: {err}')
