from django import forms

from events.models import Event

class EventForm(forms.ModelForm):
    date = forms.DateField()
    time = forms.TimeField()

    class Meta:
        model = Event
        exclude = ('slug', 'datetime', 'description_html', 'published', 'author', 'pub_date')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
