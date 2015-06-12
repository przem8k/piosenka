from django.core.urlresolvers import reverse
from django.test import TestCase

from piosenka.testing import CreateUserMixin


class InvitationTest(CreateUserMixin, TestCase):
    _LOGIN_URL = reverse('hello') + '?next=' + reverse('invite')

    def test_invite_view_get(self):
        anonymous_client = self.get_client()
        response = anonymous_client.get(reverse('invite'))
        self.assertRedirects(response, self._LOGIN_URL)  # Redirect to login.

        regular_client = self.get_client(self.create_user())
        response = regular_client.get(reverse('invite'))
        self.assertEqual(404, response.status_code)

        staff_client = self.get_client(self.create_user(is_staff=True))
        response = staff_client.get(reverse('invite'))
        self.assertEqual(200, response.status_code)

    def test_invite__view_post_empty(self):
        anonymous_client = self.get_client()
        response = anonymous_client.post(reverse('invite'), follow=True)
        self.assertRedirects(response, self._LOGIN_URL)  # Redirect to login.

        regular_client = self.get_client(self.create_user())
        response = regular_client.post(reverse('invite'))
        self.assertEqual(404, response.status_code)

        staff_client = self.get_client(self.create_user(is_staff=True))
        response = staff_client.post(reverse('invite'))
        self.assertEqual(200, response.status_code)

    def test_invite__view_post_valid(self):
        data = {'email_address': 'alice@example.com'}
        anonymous_client = self.get_client()
        response = anonymous_client.post(reverse('invite'), data, follow=True)
        self.assertRedirects(response, self._LOGIN_URL)  # Redirect to login.

        regular_client = self.get_client(self.create_user())
        response = regular_client.post(reverse('invite'), data)
        self.assertEqual(404, response.status_code)

        staff_client = self.get_client(self.create_user(is_staff=True))
        response = staff_client.post(reverse('invite'), data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('index'))  # Redirect on success.
