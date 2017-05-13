from datetime import timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from base import testing
from piosenka.models import Invitation


class InvitationTest(TestCase):
    _INVITE_LOGIN_URL = reverse('hello') + '?next=' + reverse('invite')
    _JOIN_DATA = {'username': 'Alice',
                  'first_name': 'Alice',
                  'last_name': 'Doe',
                  'password': 'secret',
                  'password_again': 'secret'}

    def test_invite_view_get(self):
        anonymous_client = testing.get_client()
        response = anonymous_client.get(reverse('invite'))
        self.assertRedirects(response, self._INVITE_LOGIN_URL)

        regular_client = testing.get_client(testing.create_user())
        response = regular_client.get(reverse('invite'))
        self.assertEqual(403, response.status_code)

        allowed_client = testing.get_client(testing.create_user(
            perms=['piosenka.invite']))
        response = allowed_client.get(reverse('invite'))
        self.assertEqual(200, response.status_code)

    def test_invite_view_post_empty(self):
        anonymous_client = testing.get_client()
        response = anonymous_client.post(reverse('invite'), follow=True)
        self.assertRedirects(response, self._INVITE_LOGIN_URL)

        regular_client = testing.get_client(testing.create_user())
        response = regular_client.post(reverse('invite'))
        self.assertEqual(403, response.status_code)

        allowed_client = testing.get_client(testing.create_user(
            perms=['piosenka.invite']))
        response = allowed_client.post(reverse('invite'))
        self.assertEqual(200, response.status_code)

    def test_invite_view_post_valid(self):
        email_address = 'alice@example.com'
        data = {'email_address': email_address}
        self.assertEqual(
            0, len(Invitation.objects.filter(email_address=email_address)))

        anonymous_client = testing.get_client()
        response = anonymous_client.post(reverse('invite'), data, follow=True)
        self.assertRedirects(response, self._INVITE_LOGIN_URL)
        self.assertEqual(
            0, len(Invitation.objects.filter(email_address=email_address)))

        regular_client = testing.get_client(testing.create_user())
        response = regular_client.post(reverse('invite'), data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            0, len(Invitation.objects.filter(email_address=email_address)))

        self.assertEqual(0, len(mail.outbox))
        allowed_client = testing.get_client(testing.create_user(
            perms=['piosenka.invite']))
        response = allowed_client.post(reverse('invite'), data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('index'))  # Redirect on success.

        self.assertEqual(
            1, len(Invitation.objects.filter(email_address=email_address)))
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual([email_address], mail.outbox[0].to)

    def test_join_view_get(self):
        invitation = Invitation.create_for_testing('alice@example.com',
                                                   testing.create_user())

        anonymous_client = testing.get_client()
        response = anonymous_client.get(invitation.get_invitation_url())
        self.assertEqual(200, response.status_code)

        regular_client = testing.get_client(testing.create_user())
        response = regular_client.get(invitation.get_invitation_url())
        self.assertEqual(404, response.status_code)

        allowed_client = testing.get_client(testing.create_user(
            perms=['piosenka.invite']))
        response = allowed_client.get(invitation.get_invitation_url())
        self.assertEqual(404, response.status_code)

    def test_join_view_post_empty(self):
        email_address = 'alice@example.com'
        invitation = Invitation.create_for_testing(email_address,
                                                   testing.create_user())
        self.assertTrue(invitation.is_valid)

        anonymous_client = testing.get_client()
        response = anonymous_client.post(invitation.get_invitation_url())
        self.assertEqual(200, response.status_code)

        invitation.refresh_from_db()
        self.assertTrue(invitation.is_valid)
        self.assertEqual(0, len(User.objects.filter(email=email_address)))

    def test_join_view_post_valid(self):
        email_address = 'alice@example.com'
        invitation = Invitation.create_for_testing(email_address,
                                                   testing.create_user())
        self.assertTrue(invitation.is_valid)

        anonymous_client = testing.get_client()
        response = anonymous_client.post(invitation.get_invitation_url(),
                                         self._JOIN_DATA)
        self.assertRedirects(response, reverse('index'))  # Redirect on success.

        invitation.refresh_from_db()
        self.assertFalse(invitation.is_valid)
        self.assertEqual(1, len(User.objects.filter(email=email_address)))

        new_user = User.objects.get(email=email_address)
        self.assertEqual(1, new_user.groups.count())
        self.assertEqual('everyone',
                         new_user.groups.values_list('name', flat=True)[0])

        another_client = testing.get_client()
        response = another_client.post(invitation.get_invitation_url(),
                                       self._JOIN_DATA)
        self.assertEqual(404, response.status_code)

        response = another_client.get(invitation.get_invitation_url())
        self.assertEqual(404, response.status_code)

    def test_join_view_expired(self):
        email_address = 'alice@example.com'
        invitation = Invitation.create_for_testing(email_address,
                                                   testing.create_user())
        invitation.expires_on = timezone.now() - timedelta(days=1)
        invitation.save()
        self.assertTrue(invitation.is_valid)

        anonymous_client = testing.get_client()
        response = anonymous_client.post(invitation.get_invitation_url(),
                                         self._JOIN_DATA)
        self.assertEqual(404, response.status_code)

        invitation.refresh_from_db()
        self.assertTrue(invitation.is_valid)
        self.assertEqual(0, len(User.objects.filter(email=email_address)))
