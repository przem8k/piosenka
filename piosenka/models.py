import hashlib
import random
from datetime import timedelta

from django import urls
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def _get_default_invitation_key():
    text_to_hash = str(random.random())
    h = hashlib.sha256(text_to_hash.encode('utf-8'))
    return h.hexdigest()


def _get_default_expires_on():
    return timezone.now() + timedelta(days=7)


class Invitation(models.Model):
    """Represents an invitation to create a contributor profile (site user)."""
    email_address = models.EmailField()
    invitation_key = models.CharField(max_length=70,
                                      editable=False,
                                      default=_get_default_invitation_key)
    expires_on = models.DateTimeField(editable=False,
                                      default=_get_default_expires_on)
    is_valid = models.BooleanField(default=True, editable=False)
    extended_by = models.ForeignKey(User, editable=False,
                                    on_delete=models.CASCADE)

    class Meta:
        permissions = [('invite', 'Can invite new contributors')]

    @staticmethod
    def create_for_testing(email_address, extended_by):
        invitation = Invitation()
        invitation.email_address = email_address
        invitation.extended_by = extended_by
        invitation.save()
        return invitation

    def get_invitation_url(self):
        return urls.reverse('join', kwargs={'invitation_key': self.invitation_key})

    def __str__(self):
        return self.email_address


class Permissions(models.Model):
    """Dummy model used to define additional permissions not tied to a
    particular model.
    """

    class Meta:
        default_permissions = []
        permissions = [('inspect', 'Has access to debug views.')]
