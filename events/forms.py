from datetime import date

from django import forms
from django.conf import settings
from pygeocoder import Geocoder
from pygeolib import GeocoderError

from events.models import ExternalEvent


class ExternalEventForm(forms.ModelForm):

    class Meta:
        model = ExternalEvent
        exclude = []
        widgets = {
            'starts_on':
                forms.widgets.DateInput(
                    format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        if 'starts_on' in cleaned_data:
            if cleaned_data['starts_on'] < date.today():
                raise forms.ValidationError(
                    'Nie można dodać wydarzenia w przeszłości')

        if 'town' in cleaned_data:
            try:
                if settings.GOOGLE_API_SERVER_KEY:
                    geocoder = Geocoder(api_key=settings.GOOGLE_API_SERVER_KEY)
                    geo = geocoder.geocode(cleaned_data['town'])
                else:
                    geo = Geocoder.geocode(cleaned_data['town'])
                cleaned_data['lat'], cleaned_data['lon'] = geo[0].coordinates
            except GeocoderError:
                # Geo lookup failed to recognize this address.
                pass
        return cleaned_data
