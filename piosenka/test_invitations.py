from django.core.urlresolvers import reverse
from django.test import TestCase

from piosenka.testing import CreateUserMixin
from piosenka.models import Invitation


class InvitationTest(CreateUserMixin, TestCase):
    _INVITE_LOGIN_URL = reverse('hello') + '?next=' + reverse('invite')

    def test_invite_view_get(self):
        anonymous_client = self.get_client()
        response = anonymous_client.get(reverse('invite'))
        self.assertRedirects(response, self._INVITE_LOGIN_URL)

        regular_client = self.get_client(self.create_user())
        response = regular_client.get(reverse('invite'))
        self.assertEqual(404, response.status_code)

        staff_client = self.get_client(self.create_user(is_staff=True))
        response = staff_client.get(reverse('invite'))
        self.assertEqual(200, response.status_code)

    def test_invite_view_post_empty(self):
        anonymous_client = self.get_client()
        response = anonymous_client.post(reverse('invite'), follow=True)
        self.assertRedirects(response, self._INVITE_LOGIN_URL)

        regular_client = self.get_client(self.create_user())
        response = regular_client.post(reverse('invite'))
        self.assertEqual(404, response.status_code)

        staff_client = self.get_client(self.create_user(is_staff=True))
        response = staff_client.post(reverse('invite'))
        self.assertEqual(200, response.status_code)

    def test_invite_view_post_valid(self):
        data = {'email_address': 'alice@example.com'}
        anonymous_client = self.get_client()
        response = anonymous_client.post(reverse('invite'), data, follow=True)
        self.assertRedirects(response, self._INVITE_LOGIN_URL)

        regular_client = self.get_client(self.create_user())
        response = regular_client.post(reverse('invite'), data)
        self.assertEqual(404, response.status_code)

        staff_client = self.get_client(self.create_user(is_staff=True))
        response = staff_client.post(reverse('invite'), data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('index'))  # Redirect on success.

    def test_join_view_get(self):
        invitation = Invitation.create_for_testing(
            'alice@example.com', self.create_user(is_staff=True))

        anonymous_client = self.get_client()
        response = anonymous_client.get(invitation.get_invitation_url())
        self.assertEqual(200, response.status_code)

        regular_client = self.get_client(self.create_user())
        response = regular_client.get(invitation.get_invitation_url())
        self.assertEqual(404, response.status_code)

        staff_client = self.get_client(self.create_user(is_staff=True))
        response = staff_client.get(invitation.get_invitation_url())
        self.assertEqual(404, response.status_code)
