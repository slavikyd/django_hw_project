"""Forms tester module."""
from django.test import TestCase

from dot_app.forms import Registration

P1 = 'password1'
P2 = 'password2'


class TestRegistrationForm(TestCase):
    """Registration form tester case.

    Args:
        TestCase (_type_): django tests inheritance.
    """

    _valid_attrs = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        P1: 'Gnkjhdfj8890',
        P2: 'Gnkjhdfj8890',
        'email': 'sirius@sirius.ru',
    }
    _not_nullable_fields = ('username', P1, P2)

    def test_empty(self):
        """Empty attrs tester."""
        for field in self._not_nullable_fields:
            attrs = self._valid_attrs.copy()
            attrs[field] = ''
            self.assertFalse(Registration(data=attrs).is_valid())

    def test_invalid_email(self):
        """Invalid email tester."""
        attrs = self._valid_attrs.copy()
        attrs['email'] = 'Huh?'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_different_password(self):
        """Not matching passwords tester."""
        attrs = self._valid_attrs.copy()
        attrs[P1] = 'JHfdshkfdfkhs71239217'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_common_password(self):
        """Common password tester."""
        attrs = self._valid_attrs.copy()
        attrs[P1] = attrs[P2] = 'Abcde123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_numeric_password(self):
        """Non valid password tester."""
        attrs = self._valid_attrs.copy()
        attrs[P1] = attrs[P2] = '123456789'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_short_password(self):
        """Short password tester."""
        attrs = self._valid_attrs.copy()
        attrs[P1] = attrs[P2] = 'ABC123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_successful(self):
        """Valid case tester."""
        self.assertTrue(Registration(data=self._valid_attrs).is_valid())
