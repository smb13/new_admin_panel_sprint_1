"""Admin module."""
from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin class for genre table."""

    # Отображение полей в списке
    list_display = ('name', 'description')

    # Поиск по полям
    search_fields = ('name', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin class for person table."""

    # Отображение полей в списке
    list_display = ('full_name',)

    # Поиск по полям
    search_fields = ('full_name', 'id')


class GenreFilmworkInline(admin.TabularInline):
    """Admin class for genre film_work inline form."""

    model = GenreFilmWork


class PersonFilmworkInline(admin.TabularInline):
    """Admin class for person film_work inline form."""

    model = PersonFilmWork


@admin.register(FilmWork)
class FilmworkAdmin(admin.ModelAdmin):
    """Admin class for film_work table."""

    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    date_hierarchy = "creation_date"

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating')

    # Фильтрация в списке
    list_filter = ('type',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id')
