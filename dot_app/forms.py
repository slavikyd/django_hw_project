from django.forms import Form, ChoiceField, CharField, DecimalField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

choices = (
    ('brd', 'board'),
    ('per', 'peripheral'),
)

class TestForm(Form):
    choice = ChoiceField(choices=choices)
    text = CharField(max_length=100)
    number = DecimalField(decimal_places=2, max_digits=10)

class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']