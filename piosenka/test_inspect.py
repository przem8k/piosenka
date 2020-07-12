"""Tests special debug pages."""

from django.test import TestCase
from django.urls import reverse

from base import testing


class InspectUrlTest(TestCase):

    def test_site_urls(self):
        login_url = reverse('hello') + '?next=' + reverse('inspect_permissions')
        response = testing.get_public_client().get(
            reverse('inspect_permissions'))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, login_url)

        response = testing.get_user_client().get(reverse('inspect_permissions'))
        self.assertEqual(403, response.status_code)

        user = testing.create_user(perms=['piosenka.inspect'])
        response = testing.get_user_client(user).get(
            reverse('inspect_permissions'))
        self.assertEqual(200, response.status_code)
