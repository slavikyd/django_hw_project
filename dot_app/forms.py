"""File for different forms in admin panel."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, ChoiceField, DecimalField, Form

choices = (
    ('brd', 'board'),
    ('per', 'peripheral'),
)


class TestForm(Form):
    """Form for tests creation.

    Args:
        Form (_type_): django base inheritance
    """

    choice = ChoiceField(choices=choices)
    text = CharField(max_length=100)
    number = DecimalField(decimal_places=2, max_digits=10)


class Registration(UserCreationForm):
    """Form for registration for user.

    Args:
        UserCreationForm (_type_): django base inheritance.
    """

    class Meta:
        """Settings subclass."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
