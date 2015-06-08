from django.forms import ModelForm

from piosenka.models import Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = []
