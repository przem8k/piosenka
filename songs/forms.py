from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from songs.models import EntityContribution, Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = []


class FirstRequiredInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(FirstRequiredInlineFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False

ContributionFormSet = inlineformset_factory(Song, EntityContribution, exclude=[],
                                            formset=FirstRequiredInlineFormSet)
