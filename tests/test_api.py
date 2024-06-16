"""Api tester module."""
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from dot_app.models import Board, Manufacturer, Subtype

URL = '/api/'
TEST = 'test'
ADMIN = 'admin'

BoardPOSTData = {'title': 'TestBoard'}
ManufacturerPOSTData = {'title': 'TestManufacturer'}
SubtypePOSTData = {'name': 'TestSubtype'}
BoardURLTemplate = 'boards/'
ManufacturerURLTemplate = 'manufacturers/'
SubtypeURLTemplate = 'subtypes/'


def api_test(model, url, creation_attributes):
    """REST methods tests creator.

    Args:
        model (_type_): model class
        url (_type_): url to api page of model
        creation_attributes (_type_): required attrs for creation

    Returns:
        TestForApi: test case for django to handle
    """
    class TestForApi(TestCase):
        """Api tester class.

        Args:
            TestCase (_type_): django test inheritance
        """

        def setUp(self) -> None:
            """Set upper base method."""
            self.client = APIClient()
            self.user = User.objects.create(username=TEST, password=TEST)
            self.superuser = User.objects.create(
                username=ADMIN, password=ADMIN, is_superuser=True,
            )
            self.user_token = Token(user=self.user)
            self.superuser_token = Token(user=self.superuser)

        def manage(
            self,
            user: User,
            token: Token,
            post_expected: int,
            put_expected: int,
            delete_expected: int,
        ):
            """Inner logic of test creator.

            Args:
                user (User): test user
                token (Token): auth token
                post_expected (int): expected code answer for post method
                put_expected (int): expected code answer for put method
                delete_expected (int): expected code answer for delete method
            """
            self.client.force_authenticate(user=user, token=token)

            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.head(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)

            self.assertEqual(
                self.client.post(url, creation_attributes).status_code, post_expected,
            )

            created_id = model.objects.create(**creation_attributes).id
            instance_url = f'{url}{created_id}/'
            put_response = self.client.put(instance_url, creation_attributes)
            self.assertEqual(put_response.status_code, put_expected)

            delete_response = self.client.delete(instance_url, creation_attributes)
            self.assertEqual(delete_response.status_code, delete_expected)

        def test_superuser(self):
            """Superuser tester case."""
            self.manage(
                self.superuser,
                self.superuser_token,
                post_expected=status.HTTP_201_CREATED,
                put_expected=status.HTTP_200_OK,
                delete_expected=status.HTTP_204_NO_CONTENT,
            )

        def test_user(self):
            """Regular user tester case."""
            self.manage(
                self.user,
                self.user_token,
                post_expected=status.HTTP_403_FORBIDDEN,
                put_expected=status.HTTP_403_FORBIDDEN,
                delete_expected=status.HTTP_403_FORBIDDEN,
            )

    return TestForApi


BoardApiTest = api_test(Board, f'{URL}{BoardURLTemplate}', BoardPOSTData)
ManufacturerApiTest = api_test(
    Manufacturer, f'{URL}{ManufacturerURLTemplate}', ManufacturerPOSTData,
)
SubtypeApiTest = api_test(Subtype, f'{URL}{SubtypeURLTemplate}', SubtypePOSTData)
