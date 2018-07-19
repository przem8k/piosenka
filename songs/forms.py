from django import forms
from django.forms.models import inlineformset_factory

from songs import models


class ArtistForm(forms.ModelForm):

    class Meta:
        model = models.Artist
        exclude = []
        widgets = {
            'born_on':
            forms.DateInput(
                format=('%d.%m.%Y'), attrs={'placeholder': 'DD.MM.RRRR'}),
            'died_on':
            forms.DateInput(
                format=('%d.%m.%Y'), attrs={'placeholder': 'DD.MM.RRRR'}),
        }


class SongForm(forms.ModelForm):

    class Meta:
        model = models.Song
        exclude = []


ContributionFormSet = inlineformset_factory(
    models.Song,
    models.EntityContribution,
    exclude=[],
    min_num=1,
    validate_min=True)


class ArtistNoteForm(forms.ModelForm):

    class Meta:
        model = models.ArtistNote
        exclude = []


class SongNoteForm(forms.ModelForm):

    class Meta:
        model = models.SongNote
        exclude = []
