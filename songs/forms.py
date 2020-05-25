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

    def set_artist_for_slug(self, artist_for_slug):
        self.artist_for_slug = artist_for_slug

    def clean(self):
        data = super().clean()
        data['artist_for_slug'] = self.artist_for_slug
        return data


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

    def set_artist(self, artist):
        self.artist = artist

    def clean(self):
        data = super().clean()
        if self.artist:
            data['artist'] = self.artist
        return data


class SongNoteForm(forms.ModelForm):

    class Meta:
        model = models.SongNote
        exclude = []
        widgets = {
            'date':
                forms.widgets.DateInput(
                    format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def set_song(self, song):
        self.song = song

    def clean(self):
        data = super().clean()
        if self.song:
            data['song'] = self.song
        return data
