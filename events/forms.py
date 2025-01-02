from datetime import date

from django import forms
from django.conf import settings

from events.models import ExternalEvent


class ExternalEventForm(forms.ModelForm):
    class Meta:
        model = ExternalEvent
        exclude = []
        widgets = {
            "starts_on": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        if "starts_on" in cleaned_data:
            if cleaned_data["starts_on"] < date.today():
                raise forms.ValidationError("Nie można dodać wydarzenia w przeszłości")

        return cleaned_data
