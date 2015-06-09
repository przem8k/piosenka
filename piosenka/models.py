from django.db import models
from django.contrib.auth.models import User


class Invitation(models.Model):
    """Represents an invitation to create a contributor profile (site user)."""
    email_address = models.EmailField()
    invitation_key = models.CharField(max_length=70, editable=False)
    expires_on = models.DateTimeField(editable=False)
    is_valid = models.BooleanField(default=True, editable=False)
    extended_by = models.ForeignKey(User, editable=False)

    @models.permalink
    def get_invitation_url(self):
        return ('join', (), {'invitation_key': self.invitation_key})

    def __str__(self):
        return self.email_address
