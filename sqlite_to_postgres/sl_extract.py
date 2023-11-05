"""Module processes extracting data from SQLite DB."""
from sqlite_to_postgres.data_classes import prepare_dict
from sqlite_to_postgres.db_settings import ROWS_IO_BUFFER
from sqlite_to_postgres.logger import get_logger


class SQLiteExtractor:
    """Class to extract data from SQLite DB."""

    def __init__(self, connection):
        """Initialise SQLiteExtractor object.

        Args:
            connection: connection to SQLite DB
        """
        self.connection = connection
        self.logger = get_logger('SQLiteExtractor')

    def extract_data(self, table_name: str, table_class: object.__class__) -> list:
        """Extract data from SQLite DB.

        Args:
            table_name: table name to extract
            table_class: corresponding dataclass to store data

        Returns:
            list: list of dataclass objects
        """
        try:
            cursor = self.connection.cursor()
            query_template = 'SELECT * FROM {table_name}'
            cursor.execute(query_template.format(table_name=table_name))
            data = []
            while True:
                result = cursor.fetchmany(ROWS_IO_BUFFER)
                if len(result) == 0:
                    break
                for row in result:
                    dict_row = prepare_dict(row)
                    data.append(table_class(**dict_row))
            self.logger.info(f'Loading from SQLite content.{table_name} database finished successfully')
            return data
        except Exception as err:
            self.logger.error(f'Error during loading from SQLite content.{table_name} database: {err}')
