from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from dot_app import models

def create_successful_page_test(page_url, page_name, template, auth=True):
    """_summary_

    Args:
        page_url: url for tested page
        page_name: name of tested page
        template: link to template file of tested page
        auth: bool value for having or not having authentication. Defaults to True.
    
    Returns:
        tset: inner func that creates test user and model and asserts generated page with template.
    """
    def test(self):
        self.client = Client()
        if auth:
            user = User.objects.create(username='user', password='user')
            models.Client.objects.create(user=user)
            self.client.force_login(user)

        reversed_url = reverse(page_name)
        url = page_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTemplateUsed(response, template)

        response = self.client.get(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    return test

def create_redirect_page_test(page_name):
    """_summary_

    Args:
        page_name: name for the tested page.
    
    Returns:
        test: inner func that check if logged out client gets needed http response.
    """
    def test(self):
        self.client = Client()
        self.client.logout()

        self.assertEqual(self.client.get(reverse(page_name)).status_code, status.HTTP_302_FOUND)

    return test

auth_pages = (
    ('/boards/', 'boards', 'catalog/boards.html'),
    ('/manufacturers/', 'manufacturers', 'catalog/manufacturers.html'),
    ('/subtypes/', 'subtypes', 'catalog/subtypes.html'),
    ('/board/', 'board', 'entities/board.html'),
    ('/manufacturer/', 'manufacturer', 'entities/manufacturer.html'),
    ('/subtype/', 'subtype', 'entities/subtype.html'),
    ('/profile/', 'profile', 'pages/profile.html'),
)

regular_pages = (
    ('/register/', 'register', 'registration/register.html'),
    ('', 'homepage', 'index.html'),
    ('/accounts/login/', 'login', 'registration/login.html'),
)




TestRegPages = type(
    'TestCasualPages', 
    (TestCase,), 
    {
        f'test_{page[1]}': create_successful_page_test(*page) for page in regular_pages
        },
                    )
TestAuthPages = type(
    'TestAuthPages',
    (TestCase,),
    {
        f'test_{page[1]}': create_successful_page_test(*page) for page in auth_pages
        }
                    )
TestNoAuthPages = type(
    'TestNoAuthPages',
    (TestCase,),
    {
    f'test_{page}': create_redirect_page_test(page) for _, page, _ in auth_pages
        }
                       )
