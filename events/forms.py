from django import forms
from django.forms.models import ModelForm, inlineformset_factory

from artists.models import Entity
from events.models import EntityPerformance, Event, Venue


class EventForm(forms.ModelForm):
    date = forms.DateField(help_text="Dzień w formacie DD.MM.RRRR, np '22.03.2014'.",
                           widget=forms.TextInput(attrs={'placeholder': 'DD.MM.RRRR'}))
    time = forms.TimeField(help_text="Godzina w formacie GG:MM, np. '20:00'.",
                           widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}))
    venue_selection = forms.ModelChoiceField(required=False, queryset=Venue.objects.all())
    venue_name = forms.CharField(required=False, max_length=100,
                                 help_text="Nazwa miejsca, np. 'Klub studencki Żaczek'.")
    venue_town = forms.CharField(required=False, max_length=100,
                                 help_text="Nazwa miasta lub miejscowości, np. 'Kraków', "
                                           "'Kołobrzeg'.")
    venue_street = forms.CharField(required=False, max_length=100,
                                   help_text="Adres w ramach miasta, np. 'ul. Podwale 37/38'.")

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        venue = cleaned_data['venue_selection'] if 'venue_selection' in cleaned_data else None
        name = cleaned_data['venue_name']
        town = cleaned_data['venue_town']
        street = cleaned_data['venue_street']
        if not venue:
            lacking = False
            msg = "To pole jest wymagane."

            if not name:
                self._errors['venue_name'] = self.error_class([msg])
                del cleaned_data['venue_name']
                lacking = True
            if not town:
                self._errors['venue_town'] = self.error_class([msg])
                del cleaned_data['venue_town']
                lacking = True
            if not street:
                self._errors['venue_street'] = self.error_class([msg])
                del cleaned_data['venue_street']
                lacking = True

            if lacking:
                self._errors['venue_selection'] = self.error_class([msg])
            else:
                venue = Venue()
                venue.name = name
                venue.town = town
                venue.street = street
                try:
                    venue.clean()
                except forms.ValidationError:
                    geo_msg = "Nie udało się zlokalizować adresu."
                    self._errors['venue_street'] = self.error_class([geo_msg])
                    del cleaned_data['venue_street']
        else:
            if name or town or street:
                raise forms.ValidationError("Stało się coś dziwnego.")
        cleaned_data['venue'] = venue
        return cleaned_data

    class Meta:
        model = Event
        exclude = ['venue', 'datetime']


class EntityPerformanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntityPerformanceForm, self).__init__(*args, **kwargs)
        self.fields['entity'].queryset = Entity.objects.filter(still_plays=True)

    class Meta:
        model = EntityPerformance
        exclude = []


PerformanceFormSet = inlineformset_factory(Event, EntityPerformance, form=EntityPerformanceForm,
                                           exclude=[])
