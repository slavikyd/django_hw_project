from django.db import models
from uuid import uuid4
from datetime import datetime, date, timezone
from django.core.exceptions import ValidationError


def get_datetime():
    return datetime.now(timezone.utc)

def check_created(time_: datetime):
    if time_ > get_datetime():
        raise ValidationError(('Date and time is bigger than current!'), params={'created': time_})

def check_modified(time_: datetime):
    if time_ > get_datetime():
        raise ValidationError(('Date and time is bigger than current!'),params={'modified': time_})

def check_year(year: int):
    start_year = 1930
    end_year = get_datetime().year + 10
    if year not in range(start_year, end_year+1):
        raise ValidationError(('Not valid board release year entered! Check what you typed in!'), params={'year': year})

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True

class CreatedMixin(models.Model):
    created = models.DateTimeField(null=True, blank=True, default=datetime.now, validators=[check_created,])

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(null=True, blank=True, default=datetime.now, validators=[check_modified,])

    class Meta:
        abstract = True

class Manufacturer(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(null=False, blank=False)

    boards = models.ManyToManyField('Board', through='BoardManufacturer')

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = '"databank"."Manufacturer"'

class Subtype(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = '"databank"."subtype"'


class Board(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True, validators=[check_year,])
    
    subtypes = models.ManyToManyField(Subtype, through='BoardSubtype')
    manufacturers = models.ManyToManyField(Manufacturer, through='BoardManufacturer')

    def __str__(self) -> str:
        return f'{self.title}, {self.year}, {self.type} pages'

    class Meta:
        db_table = '"databank"."Board"'

class BoardBoard(UUIDMixin, CreatedMixin):
    connection_choices = {
        'USB/UART': 'USB with UART support',
        'USB/COM': 'USB with COM support',
        'USB': 'plain USB',
        'USB-C:USB-A': 'USB-C to USB-A connection',
        'USB-Micro:USB-A': 'Micro USB to USB-A connection', 
    }
    theboard = models.ForeignKey(Board, on_delete=models.CASCADE)
    compatibleboard = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='compatible_type_board')
    connections = models.TextField(null=False, blank=False, default='USB/COM', choices=connection_choices)

class BoardSubtype(UUIDMixin, CreatedMixin):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    subtype = models.ForeignKey(Subtype, on_delete=models.CASCADE)

    class Meta:
        db_table = '"databank"."board_subtype"'
        unique_together = (
            ('board', 'subtype'),
        )

class BoardManufacturer(UUIDMixin, CreatedMixin):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        db_table = '"databank"."board_manufacturer"'
        unique_together = (
            ('board', 'manufacturer'),
        )

