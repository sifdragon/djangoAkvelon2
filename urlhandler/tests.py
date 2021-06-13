from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class UrlViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('test', 'test@mail.ru', 'test')

    def test_dashboard_not_allowed_unauthorized(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_allowed_authorized(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
