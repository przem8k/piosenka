from django.db import models


class Invitation(models.Model):
    """Represents an invitation to create a contributor profile (site user)."""
    email_address = models.EmailField()
    invitation_key = models.CharField(max_length=70, editable=False)
    expires_on = models.DateTimeField(editable=False)
