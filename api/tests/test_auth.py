from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .factories import UserFactory
import factory.random
import json


class LoginTest(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.user = UserFactory.create()
        self.client = APIClient()

    def test_success(self):
        response = self.client.post('/api/v1/login', {
            'email': 'ronniepeterson@gmail.com',
            'password': 'password'
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('key' in content)

    def test_failure(self):
        response = self.client.post('/api/v1/login', {
            'email': 'foo@example.com',
            'password': 'wrong-password'
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertFalse('key' in content)
        self.assertEqual(
            content.get('non_field_errors'),
            ['Unable to log in with provided credentials.']
        )


class LogoutTest(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        user = UserFactory.create()
        token = Token.objects.create(user=user)
        self.client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_success(self):
        response = self.client.post('/api/v1/logout')
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.count(), 0)
        self.assertEqual(
            content.get('detail'),
            'Successfully logged out.'
        )


class RegisterTest(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()

    def test_success(self):
        response = self.client.post('/api/v1/register', {
            'email': 'dan@example.com',
            'password1': 'hax0r ftw',
            'password2': 'hax0r ftw',
        })
        content = json.loads(response.content)
        self.assertTrue('key' in content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_multiple(self):
        self.client.post('/api/v1/register', {
            'email': 'dan1@example.com',
            'password1': 'hax0r ftw',
            'password2': 'hax0r ftw',
        })
        self.client.post('/api/v1/register', {
            'email': 'dan2@example.com',
            'password1': 'hax0r ftw',
            'password2': 'hax0r ftw',
        })
        self.assertEqual(User.objects.count(), 2)
