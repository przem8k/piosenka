from django import forms

from events.models import Event, Venue


class EventForm(forms.ModelForm):
    date = forms.DateField(
        help_text="Dzień w formacie DD.MM.RRRR, np '22.03.2014'.",
        widget=forms.TextInput(attrs={'placeholder': 'DD.MM.RRRR'}))
    time = forms.TimeField(
        help_text="Godzina w formacie GG:MM, np. '20:00'.",
        widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}))
    venue_selection = forms.ModelChoiceField(
        required=False, queryset=Venue.objects.all())
    venue_name = forms.CharField(
        required=False,
        max_length=100,
        help_text="Nazwa miejsca, np. 'Klub studencki Żaczek'.")
    venue_town = forms.CharField(
        required=False,
        max_length=100,
        help_text="Nazwa miasta lub miejscowości, np. 'Kraków', 'Kołobrzeg'.")
    venue_street = forms.CharField(
        required=False,
        max_length=100,
        help_text="Adres w ramach miasta, np. 'ul. Podwale 37/38'.")

    def clean(self):
        cleaned_data = super().clean()

        venue = None
        if 'venue_selection' in cleaned_data:
            venue = cleaned_data['venue_selection']

        if not venue:
            name = cleaned_data['venue_name']
            town = cleaned_data['venue_town']
            street = cleaned_data['venue_street']
            if name and town and street:
                venue = Venue()
                venue.name = name
                venue.town = town
                venue.street = street
                venue.clean()
            else:
                self.add_error('venue_selection', 'Wybierz miejsce z listy '
                               'lub wypełnij formularz aby dodać nowe miejsce.')

        cleaned_data['venue'] = venue
        return cleaned_data

    class Meta:
        model = Event
        exclude = ['venue', 'datetime']
