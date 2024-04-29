from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Board, Subtype, Manufacturer, BoardManufacturer, BoardSubtype, BoardBoard
from datetime import date
from django.utils.translation import gettext_lazy as _

class RecencyBoardFilter(admin.SimpleListFilter):
    title = _('recency')
    parameter_name = 'recency'
    _five_yo = '5yo'
    _ten_yo = '10yo'
    _fifteen_yo = '15yo'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[str, str]]:
        return (
            (self._five_yo, _('Released in last 5 years')),
            (self._ten_yo, _('Created in the last 10 years')),
            (self._fifteen_yo, _('Created in the last 15 years')),

        )
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        decade = 10
        year_today = date.today().year
        if self.value() == self._five_yo:
            return queryset.filter(year__gte=year_today-(decade/2))
        elif self.value() == self._ten_yo:
            return queryset.filter(year__gte=year_today-decade)
        elif self.value() == self._ten_yo:
            return queryset.filter(year__gte=year_today-(decade+(decade/2))) # TODO remove this scary thing
        return queryset

class BoardManufacturerInline(admin.TabularInline):
    model = BoardManufacturer
    extra = 1
    
class BoardSubtypeInline(admin.TabularInline):
    model = BoardSubtype
    extra = 1

class BoardBoardInline(admin.TabularInline):
    model = BoardBoard
    extra = 1

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
    inlines = (BoardManufacturerInline,)

@admin.register(Subtype)
class SubtypeAdmin(admin.ModelAdmin):
    model = Subtype

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    model = Board
    inlines = (BoardManufacturerInline, BoardSubtypeInline)
    list_filter = (
        'type',
        'subtypes',
        RecencyBoardFilter,
    )

@admin.register(BoardSubtype)
class BoardSubtypeAdmin(admin.ModelAdmin):
    model = BoardSubtype

@admin.register(BoardManufacturer)
class BoardManufacturerAdmin(admin.ModelAdmin):
    model = BoardManufacturer

@admin.register(BoardBoard)
class BoardBoardAdmin(admin.ModelAdmin):
    model = BoardBoard
