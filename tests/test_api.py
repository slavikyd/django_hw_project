from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token

from dot_app.models import Board, Manufacturer, Subtype
URL = '/api/'

BoardPOSTData = {'title': 'TestBoard'}
ManufacturerPOSTData = {'title': 'TestManufacturer'}
SubtypePOSTData = {'name': 'TestSubtype'}
BoardURLTemplate='boards/'
ManufacturerURLTemplate='manufacturers/'
SubtypeURLTemplate='subtypes/'

def api_test(model, url, creation_attributes):
    class TestForApi(TestCase):
        def setUp(self) -> None:
            self.client = APIClient()
            self.user = User.objects.create(username='test', password='test')
            self.superuser = User.objects.create(username='admin', password='admin', is_superuser=True)
            self.user_token = Token(user=self.user)
            self.superuser_token = Token(user=self.superuser)
        
        def manage(self, user: User, token: Token, post_expected: int, put_expected: int, delete_expected: int):
            self.client.force_authenticate(user=user, token=token)

            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.head(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)

            self.assertEqual(self.client.post(url, creation_attributes).status_code, post_expected)
            
            created_id = model.objects.create(**creation_attributes).id
            instance_url = f'{url}{created_id}/'
            put_response = self.client.put(instance_url, creation_attributes)
            self.assertEqual(put_response.status_code, put_expected)

            delete_response = self.client.delete(instance_url, creation_attributes)
            self.assertEqual(delete_response.status_code, delete_expected)

        def test_superuser(self):
            self.manage(
                self.superuser, self.superuser_token,
                post_expected=status.HTTP_201_CREATED,
                put_expected=status.HTTP_200_OK,
                delete_expected=status.HTTP_204_NO_CONTENT,
            )

        def test_user(self):
            self.manage(
                self.user, self.user_token,
                post_expected=status.HTTP_403_FORBIDDEN,
                put_expected=status.HTTP_403_FORBIDDEN,
                delete_expected=status.HTTP_403_FORBIDDEN,
            )
    return TestForApi

BoardApiTest = api_test(Board, f'{URL}{BoardURLTemplate}', BoardPOSTData)
ManufacturerApiTest = api_test(Manufacturer, f'{URL}{ManufacturerURLTemplate}', ManufacturerPOSTData)
SubtypeApiTest = api_test(Subtype, f'{URL}{SubtypeURLTemplate}', SubtypePOSTData)
