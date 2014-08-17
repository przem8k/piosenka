from django import forms
from django.forms.models import inlineformset_factory

from songs.models import EntityContribution, Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = ()

ContributionFormSet = inlineformset_factory(Song, EntityContribution)
