"""Module declare dataclasses to load data from SQLite to Postgres."""
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime


def prepare_dict(row: sqlite3.Row) -> dict:
    """Prepare date for Postgres to load.

    Args:
        row: row data from sqlite3 table

    Returns:
        dict: dictionary with correct keys for Postgres table
    """
    row_dict = dict(row)
    if 'created_at' in row_dict:
        row_dict['created'] = row_dict.pop('created_at')
    if 'updated_at' in row_dict:
        row_dict['modified'] = row_dict.pop('updated_at')
    if 'file_path' in row_dict:
        row_dict.pop('file_path')
    return row_dict


@dataclass(frozen=True)
class FilmWork(object):
    """Class for data from film_work table."""

    title: str
    description: str
    creation_date: datetime
    type: str
    created: datetime
    modified: datetime
    rating: float = field(default=0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person(object):
    """Class for data from person table."""

    full_name: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre(object):
    """Class for data from genre table."""

    name: str
    description: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreFilmWork(object):
    """Class for data from genre_film_work table."""

    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonFilmWork(object):
    """Class for data from person_film_work table."""

    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
