from django.db import models

def create_manager(validators: tuple[tuple[str, callable]]):
    class Manager(models.Manager):
        @staticmethod
        def check_and_validate(kwargs, value, validator):
            if value in kwargs.keys():
                validator(kwargs.get(value))

        def create(self, **kwargs):
            for value, validator in validators:
                self.check_and_validate(kwargs, value, validator)
            return super().create(**kwargs)
    return Manager

def create_save(validators: tuple[tuple[str, callable]]):
    def save(self, *args, **kwargs) -> None:
        for value, validator in validators:
            validator(getattr(self, value))
        return super(self.__class__, self).save(*args, **kwargs)

    return save
