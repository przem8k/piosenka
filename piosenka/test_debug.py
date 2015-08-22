"""Tests special debug pages."""

from django.test import TestCase
from django.core.urlresolvers import reverse

from base import testing


class DebugUrlTest(TestCase):
    def test_site_urls(self):
        response = testing.get_public_client().get(reverse('debug_locale'))
        self.assertEqual(404, response.status_code)
        response = testing.get_user_client().get(reverse('debug_locale'))
        self.assertEqual(404, response.status_code)

        user = testing.create_user(perms=['piosenka.debug'])
        response = testing.get_user_client(user).get(reverse('debug_locale'))
        self.assertEqual(200, response.status_code)
