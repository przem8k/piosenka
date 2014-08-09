from django import forms
from django.utils.text import slugify

from unidecode import unidecode

from events.models import Event, Venue

class EventForm(forms.ModelForm):
    date = forms.DateField()
    time = forms.TimeField()
    venue = forms.ModelChoiceField(queryset=Venue.objects.all())
    venue_name = forms.CharField(required=False, max_length=100)
    venue_town = forms.CharField(required=False, max_length=100)
    venue_street = forms.CharField(required=False, max_length=100)

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        venue = cleaned_data['venue']
        name = cleaned_data['venue_name']
        town = cleaned_data['venue_town']
        street = cleaned_data['venue_street']
        if not venue:
            if not name or not town or not street:
                raise forms.ValidationError('If no existing venue is selected, need to fill the '
                                            'description fields.')
            venue = Venue()
            venue.name = name
            venue.town = town
            venue.street = street
            venue.slug = slugify(unidecode(venue.name) + " " + unidecode(venue.town))
            venue.clean()
        else:
            if name or town or street:
                raise forms.ValidationError('If an existing venue is selected, the description fields '
                                            'need to be empty')
        cleaned_data['venue'] = venue
        return cleaned_data


    class Meta:
        model = Event
        exclude = ('venue', 'slug', 'datetime', 'description', 'description_html', 'published', 'author', 'pub_date')
