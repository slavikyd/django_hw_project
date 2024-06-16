"""Mixins for django.orm models."""
from uuid import uuid4

from django.db import models

from .models_funcs import get_datetime
from .models_validators import check_created, check_modified


class UUIDMixin(models.Model):
    """Mixin class for uuid field.

    Args:
        models (_type_): inheritance from django base model class.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        """Settings class."""

        abstract = True


class CreatedMixin(models.Model):
    """Mixing for adding created field into the model.

    Args:
        models (_type_): inheritance from django base model class.
    """

    created = models.DateTimeField(
        null=True,
        blank=True,
        default=get_datetime,
        validators=[check_created],
    )

    class Meta:
        """Settings class."""

        abstract = True


class ModifiedMixin(models.Model):
    """Mixin for adding modified field into the model.

    Args:
        models (_type_): inheritance from django base model class.
    """

    modified = models.DateTimeField(
        null=True,
        blank=True,
        default=get_datetime,
        validators=[check_modified],
    )

    class Meta:
        """Meta settings class."""

        abstract = True
