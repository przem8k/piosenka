import hashlib
import random
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User


def _get_default_invitation_key():
    text_to_hash = str(random.random())
    h = hashlib.sha256(text_to_hash.encode('utf-8'))
    return h.hexdigest()


def _get_default_expires_on():
    return datetime.now() + timedelta(days=7)


class Invitation(models.Model):
    """Represents an invitation to create a contributor profile (site user)."""
    email_address = models.EmailField()
    invitation_key = models.CharField(max_length=70, editable=False,
                                      default=_get_default_invitation_key)
    expires_on = models.DateTimeField(editable=False,
                                      default=_get_default_expires_on)
    is_valid = models.BooleanField(default=True, editable=False)
    extended_by = models.ForeignKey(User, editable=False)

    @staticmethod
    def create_for_testing(email_address, extended_by):
        invitation = Invitation()
        invitation.email_address = email_address
        invitation.extended_by = extended_by
        invitation.save()
        return invitation

    @models.permalink
    def get_invitation_url(self):
        return ('join', (), {'invitation_key': self.invitation_key})

    def __str__(self):
        return self.email_address
