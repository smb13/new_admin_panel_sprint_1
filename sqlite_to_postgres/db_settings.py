"""Module sets constants that need for processing databases."""
import os

import dotenv

from sqlite_to_postgres.data_classes import (FilmWork, Genre, GenreFilmWork,
                                             Person, PersonFilmWork)

dotenv.load_dotenv()
SQLITE_DB_PATH = os.path.join(os.environ.get('ROOT_PATH'), 'sqlite_to_postgres/db.sqlite')
SCHEMA = 'content'
tables_classes = {
    'person': Person,
    'genre': Genre,
    'film_work': FilmWork,
    'person_film_work': PersonFilmWork,
    'genre_film_work': GenreFilmWork,
}
ROWS_IO_BUFFER = 1000
POSTGRES_PORT = 5432
dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', POSTGRES_PORT),
}
