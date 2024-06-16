"""Validators for django.orm models."""
import datetime

from django.core.exceptions import ValidationError

from .models_funcs import get_datetime


def check_created(time_created: datetime.datetime):
    """Model validator of timestamp for model.

    Args:
        time_created (datetime): time of creation for object

    Raises:
        ValidationError: if date is bigger
    """
    if time_created > get_datetime():
        raise ValidationError(
            ('Date and time is bigger than current!'),
            params={'created': time_created},
        )


def check_modified(time_modified: datetime.datetime):
    """Model validator for of timestamp for modifying.

    Args:
        time_modified (datetime): timestamp of object modification

    Raises:
        ValidationError: if invalid timestamp given
    """
    if time_modified > get_datetime():
        raise ValidationError(
            ('Date and time is bigger than current!'),
            params={'modified': time_modified},
        )


def check_year(year: int):
    """Model validator for valid year set in model.

    Args:
        year (int): year of model (board) release.

    Raises:
        ValidationError: if year is too far from future or too far from past
    """
    start_year = 1930
    end_year = get_datetime().year + 10
    if year not in range(start_year, end_year+1):
        raise ValidationError(
            ('Not valid board release year entered! Check what you typed in!'),
            params={'year': year},
        )
