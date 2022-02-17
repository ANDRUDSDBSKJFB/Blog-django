from django.test import TestCase
from django.urls import reverse

from .models import Post


class UrlsModelTest(TestCase):
    def test_urls_reg(self):
        url = reverse('registration')
        print(url)
        response = self.client.get(url)
        print(response)

    def test_urls_auth(self):
        url = reverse('auth')
        print(url)
        response = self.client.get(url)
        print(response)
