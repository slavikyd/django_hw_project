"""Module for django admin panel intialization."""
from datetime import date
from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from . import models


class RecencyBoardFilter(admin.SimpleListFilter):
    """Filter that gives us ability to sort board by their release year.

    Args:
        admin (_type_): inheritance from base admin class

    """

    title = _('recency')
    parameter_name = 'recency'
    _five_yo = '5yo'
    _ten_yo = '10yo'
    _fifteen_yo = '15yo'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[str, str]]:
        """Similar to choice function, but from django admin panel funcs.

        Args:
            request (Any): not needed
            model_admin (Any): not needed

        Returns:
            list[tuple[str, str]]: list of boards
        """
        return (
            (self._five_yo, _('Released in last 5 years')),
            (self._ten_yo, _('Created in the last 10 years')),
            (self._fifteen_yo, _('Created in the last 15 years')),
        )

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        """Query to the database filtered by our wishes.

        Args:
            request (Any): not needed
            queryset (QuerySet[Any]): Set of queries itself

        Returns:
            QuerySet[Any] | None: boards that are loaded into dict after all
        """
        decade = 10
        year_today = date.today().year
        if self.value() == self._five_yo:
            return queryset.filter(year__gte=year_today-(decade/2))
        elif self.value() == self._ten_yo:
            return queryset.filter(year__gte=year_today-decade)
        elif self.value() == self._ten_yo:
            return queryset.filter(year__gte=year_today-(decade+(decade/2)))
            # TODO remove this scary thing
        return queryset


class BoardManufacturerInline(admin.TabularInline):
    """Inline of manytomany table of Board and Manufacturer connection.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.BoardManufacturer
    extra = 1


class BoardSubtypeInline(admin.TabularInline):
    """Inline of manytomany table of Board and Subtype connection.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.BoardSubtype
    extra = 1


class BoardBoardInline(admin.TabularInline):
    """Inline of manytomany table of Board and Board connection.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.BoardBoard
    extra = 1


@admin.register(models.Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """Registration of table Manufacturer.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.Manufacturer
    inlines = (BoardManufacturerInline,)


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    """Registration of table Client.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.Client


@admin.register(models.Subtype)
class SubtypeAdmin(admin.ModelAdmin):
    """Registration of table Subtype.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.Subtype


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    """Registration of table Board.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.Board
    inlines = (BoardManufacturerInline, BoardSubtypeInline)
    list_filter = (
        'type',
        'subtypes',
        RecencyBoardFilter,
    )


@admin.register(models.BoardSubtype)
class BoardSubtypeAdmin(admin.ModelAdmin):
    """Registration of manytomany table of Board and Subtype connection.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.BoardSubtype


@admin.register(models.BoardManufacturer)
class BoardManufacturerAdmin(admin.ModelAdmin):
    """Registration of manytomany table of Board and Manufacturer connection.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.BoardManufacturer


@admin.register(models.BoardBoard)
class BoardBoardAdmin(admin.ModelAdmin):
    """Registration of manytomany table of Board and Board connection.

    Args:
        admin (_type_): base django admin class inheritance
    """

    model = models.BoardBoard
