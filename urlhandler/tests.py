from django.contrib.auth.models import User

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from .models import shorturl


class UrlViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('test', 'test@mail.ru', 'test')

    def test_dashboard_not_allowed_unauthorized(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_no_urls(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['urls'], [])

    def test_dashboard_has_urls(self):
        user = User.objects.create_user('test1', 'test1@mail.ru', 'test1')
        self.client.login(username='test1', password='test1')
        response = self.client.get(reverse('dashboard'))
        shorturl.objects.create(original_url='test', short_query='qweqwe', user=user)
        urls = shorturl.objects.filter(user=user)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['urls'], [urls])



