from django.forms import Form, ModelForm
from django import forms

from piosenka.models import Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = []


class JoinForm(Form):
    _HELP_USERNAME = """Używana do logowania, publicznie widoczna w stopce
materiałów, które dodasz."""
    _HELP_REAL_NAME = """Widoczne publicznie w Twojej karcie w dziale "O
stronie"."""
    username = forms.CharField(label='Nazwa użytkownika', max_length=30,
                               help_text=_HELP_USERNAME)
    first_name = forms.CharField(label='Imię', max_length=30,
                                 help_text=_HELP_REAL_NAME)
    last_name = forms.CharField(label='Nazwisko', max_length=30,
                                help_text=_HELP_REAL_NAME)
    password = forms.CharField(label='Hasło', max_length=30,
                               widget=forms.PasswordInput())
    password_again = forms.CharField(label='Hasło (powtórz)', max_length=30,
                                     widget=forms.PasswordInput())
