from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase


# Create your tests here.


class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('test', 'test@mail.ru', 'test')

    def test_login(self):
        header_info = {'content-type': 'application/json'}
        dictionary = {
            'email': 'test@mail.ru',
            'password': 'test',
            'next': ''
        }
        self.client.post('/login/', headers=header_info, data=dictionary)
        user = auth.get_user(self.client)
        assert user.is_authenticated


class RegistrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('test', 'test@mail.ru', 'test')

    def test_registration(self):
        dictionary = {
            'username': 'test',
            'email': 'test@mail.ru',
            'password': 'test',
            'password2': 'test'
        }
        self.client.post('/signup/', data=dictionary)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
