from django.forms import Form, ModelForm
from django import forms

from piosenka.models import Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = []


class JoinForm(Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=30)
    first_name = forms.CharField(label='Imię', max_length=30)
    last_name = forms.CharField(label='Nazwisko', max_length=30)
    password = forms.CharField(label='Hasło', max_length=30)
    password_again = forms.CharField(label='Hasło (powtórz)', max_length=30)
