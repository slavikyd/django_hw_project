"""Models for django web-application."""
import datetime

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils.translation import gettext_lazy as _
# from django_currentuser.middleware import (
# get_current_user, get_current_authenticated_user)
from django_minio_backend import MinioBackend, iso_date_prefix

from . import choices
from .models_funcs import create_manager, create_save
from .models_mixins import CreatedMixin, ModifiedMixin, UUIDMixin
from .models_validators import check_created, check_modified, check_year


class Manufacturer(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model for manufacturer table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
        ModifiedMixin (_type_): inheritance of modified field


    """

    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=False, default='Nothing to look for here')
    boards = models.ManyToManyField('Board', through='BoardManufacturer')

    def __str__(self) -> str:
        """Representation in string, method for class.

        Returns:
            str: title of the manufacturer
        """
        return self.title

    class Meta:
        """Subclass for internal settings."""

        db_table = '"databank"."Manufacturer"'
        ordering = ['-id']


class Subtype(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model for subtype table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
        ModifiedMixin (_type_): inheritance of modified field

    """

    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        """Representation of string method for class.

        Returns:
            str: name of subtype
        """
        return self.name

    class Meta:
        """Model subclass for settings."""

        db_table = '"databank"."subtype"'
        ordering = ['-id']


class Board(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model for board table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
        ModifiedMixin (_type_): inheritance of modified field

    """

    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True, default='Undefined')
    year = models.IntegerField(
        null=True,
        blank=True,
        validators=[check_year],
        default=datetime.date.today().year,
    )
    datasheet = models.FileField(
        null=True, blank=True,
        storage=MinioBackend(bucket_name='static'),
        upload_to=iso_date_prefix,
    )
    image = models.ImageField(
        null=True, blank=True,
        storage=MinioBackend(bucket_name='static'),
        upload_to=iso_date_prefix,
    )
    subtypes = models.ManyToManyField(Subtype, through='BoardSubtype')
    manufacturers = models.ManyToManyField(Manufacturer, through='BoardManufacturer')

    def __str__(self) -> str:
        """Representation of string for class.

        Returns:
            str: _description_
        """
        return f'{self.title}, {self.year}, {self.type} pages'

    class Meta:
        """Meta settings class."""

        db_table = '"databank"."Board"'
        ordering = ['-id']


class BoardBoard(UUIDMixin, CreatedMixin):
    """Many-to-many connection table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
    """

    connection_choices = (
        (choices.UU, _('USB with UART support')),
        (choices.UC, _('USB with COM support')),
        (choices.UP, _('plain USB')),
        (choices.U_C_U_A, _('USB-C to USB-A connection')),
        (choices.U_MC_U_A, _('Micro USB to USB-A connection')),
    )
    theboard = models.ForeignKey(Board, on_delete=models.CASCADE)
    compatibleboard = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='compatible_type_board',
    )
    connections = models.TextField(
        null=False,
        blank=False,
        default='USB/COM',
        choices=connection_choices,
    )


class BoardSubtype(UUIDMixin, CreatedMixin):
    """Board to subtype many to many table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
    """

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    subtype = models.ForeignKey(Subtype, on_delete=models.CASCADE)

    class Meta:
        """Settings subclass."""

        db_table = '"databank"."board_subtype"'
        unique_together = (
            ('board', 'subtype'),
        )


class BoardManufacturer(UUIDMixin, CreatedMixin):
    """Board to manufacturer many to many table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
    """

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        """Settings subclass."""

        db_table = '"databank"."board_manufacturer"'
        unique_together = (
            ('board', 'manufacturer'),
        )


client_validators = (
    ('created', check_created), ('modified', check_modified),
)


class Client(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Model for client table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
        ModifiedMixin (_type_): inheritance of modified field

    """

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        unique=True,
        verbose_name=('user'),
        on_delete=models.CASCADE,
    )
    boards = models.ManyToManyField(Board, through='BoardClient', verbose_name=('boards'))
    cls_objects = create_manager(client_validators)
    save = create_save(client_validators)

    class Meta:
        """Settings subclass."""

        db_table = '"databank"."client"'
        verbose_name = ('client')
        verbose_name_plural = ('clients')

    @property
    def username(self) -> str:
        """Read-only property for username field.

        Returns:
            str: username
        """
        return self.user.username

    @property
    def first_name(self) -> str:
        """Read-only property for first-name field.

        Returns:
            str: user first name
        """
        return self.user.first_name

    @property
    def last_name(self) -> str:
        """Read-only property for last-name field.

        Returns:
            str: last_name of user
        """
        return self.user.last_name

    def __str__(self) -> str:
        """Representation of string method for class.

        Returns:
            str: User main info in string
        """
        return f'{self.username} ({self.first_name} {self.last_name})'


class BoardClient(UUIDMixin, CreatedMixin):
    """Board to client many-to-many table.

    Args:
        UUIDMixin (_type_): inheritance of uuid field
        CreatedMixin (_type_): inheritance of created field
    """

    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name=('board'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=('client'))

    class Meta:
        """Subclass for settings."""

        db_table = '"databank"."board_client"'
        verbose_name = _('relationship board client')
        verbose_name_plural = _('relationships boards client')
