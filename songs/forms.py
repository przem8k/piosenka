from django import forms
from django.forms.models import inlineformset_factory

from songs.models import (Artist, Annotation, ArtistNote, EntityContribution,
                          Song)


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        exclude = []
        widgets = {
            'born_on': forms.TextInput(attrs={'placeholder': 'DD.MM.RRRR'}),
            'died_on': forms.TextInput(attrs={'placeholder': 'DD.MM.RRRR'}),
        }


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        exclude = []


ContributionFormSet = inlineformset_factory(Song,
                                            EntityContribution,
                                            exclude=[],
                                            min_num=1,
                                            validate_min=True)


class AnnotationForm(forms.ModelForm):

    class Meta:
        model = Annotation
        exclude = []


class ArtistNoteForm(forms.ModelForm):

    class Meta:
        model = ArtistNote
        exclude = []
