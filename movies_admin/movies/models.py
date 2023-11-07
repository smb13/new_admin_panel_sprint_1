"""Models module."""
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Model class for created, modified fields."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""

        abstract = True


class UUIDMixin(models.Model):
    """Model class for id field."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Meta class."""

        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Model class for genre table."""

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        """Meta class."""

        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    """Model class for person table."""

    full_name = models.CharField(_('full name'), max_length=255)

    class Meta:
        """Meta class."""

        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Model class for film_work table."""

    class Type(models.TextChoices):
        """Model TextChoices class for film_work table."""

        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('type'), choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        """Meta class."""

        db_table = "content\".\"film_work"
        verbose_name = _('Film work')
        verbose_name_plural = _('Film works')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    """Model class for genre_film_work table."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class."""

        db_table = "content\".\"genre_film_work"
        unique_together = [['film_work', 'genre']]


class PersonFilmWork(UUIDMixin):
    """Model class for person_film_work table."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class."""

        db_table = "content\".\"person_film_work"
        unique_together = [['film_work', 'person', 'role']]
