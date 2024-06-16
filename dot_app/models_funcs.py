"""File with functions for django orm models."""
import datetime

from django.db import models


def create_manager(validators: tuple[tuple[str, callable]]):
    """Cool feature validator of model class.

    Args:
        validators (tuple[tuple[str, callable]]): tuple of requiered validators

    Returns:
        type: Manager instance
    """

    class Manager(models.Manager):
        """Manager model class.

        Args:
            models (_type_): django base inhertiance

        """

        @staticmethod
        def check_and_validate(kwargs, value, validator):
            """All validator method.

            Args:
                kwargs (_type_): kwargs of class
                value (_type_): desired value
                validator (_type_): validator that we need
            """
            if value in kwargs.keys():
                validator(kwargs.get(value))

        def create(self, **kwargs):
            """Create method reinstancing.

            Args:
                kwargs: base kwargs from method

            Returns:
                create method
            """
            for value, validator in validators:
                self.check_and_validate(kwargs, value, validator)
            return super().create(**kwargs)

    return Manager


def create_save(validators: tuple[tuple[str, callable]]):
    """Save reinstancing function kinda decorator.

    Args:
        validators (tuple[tuple[str, callable]]): validators for model.

    Returns:
        reinstanced save method
    """

    def save(self, *args, **kwargs) -> None:
        """Save method reinstance.

        Args:
            self: class self
            args: basic save method args
            kwargs: basic save method keywird args

        Returns:
            save: updated method
        """
        for value, validator in validators:
            validator(getattr(self, value))
        return super(self.__class__, self).save(*args, **kwargs)

    return save


def get_datetime():
    """Getter of current datetime.

    Returns:
        current datetime
    """
    return datetime.datetime.now(datetime.timezone.utc)
