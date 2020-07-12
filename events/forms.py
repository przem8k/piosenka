import logging
from datetime import date

import geocoder
from django import forms
from django.conf import settings

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
                if not settings.PIOSENKA_GOOGLE_API_GEOCODING_SERVER_KEY:
                    logging.warning(
                        'PIOSENKA_GOOGLE_API_GEOCODING_SERVER_KEY not set')
                g = geocoder.google(
                    cleaned_data['town'],
                    components="country:PL",
                    key=settings.PIOSENKA_GOOGLE_API_GEOCODING_SERVER_KEY)

                cleaned_data['lat'] = g.latlng[0]
                cleaned_data['lon'] = g.latlng[1]
            except GeocoderError:
                logging.error('Geocoder lookup failed')
                raise forms.ValidationError(
                    'Nie udało się nam odnaleźć tej miejscowości na mapie.')
        return cleaned_data
