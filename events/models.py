import uuid
from datetime import date, timedelta

from django import urls
from django.db import models
from django.urls import reverse
from django.utils import timezone
from pygeocoder import Geocoder
from pygeolib import GeocoderError

from base.overrides import overrides
from content import url_scheme
from content.models import ContentItem
from content.slug import SlugFieldMixin, SlugLogicMixin
from content.trevor import put_text_in_trevor, render_trevor


class Performer(SlugFieldMixin, models.Model):
    HELP_NAME = """Imię i nazwisko wykonawcy lub nazwa zespołu."""

    name = models.CharField(max_length=50, help_text=HELP_NAME)
    website = models.URLField(null=True, blank=True)
    fb_page_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    @staticmethod
    def create_for_testing():
        performer = Performer()
        performer.name = str(uuid.uuid4())
        performer.full_clean()
        performer.save()
        return performer

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return urls.reverse('view_performer', kwargs={'slug': self.slug})

    @overrides(SlugFieldMixin)
    def get_slug_elements(self):
        return [self.name]


class ExternalEvent(models.Model):
    HELP_NAME = 'Nazwa wydarzenia, w tym występujący artysta lub zespół.'
    HELP_STARTS_ON = 'Data rozpoczęcia wydarzenia.'
    HELP_URL = 'Strona internetowa wydarzenia (może być na Facebooku).'
    HELP_TOWN = 'Miejscowość w którym odbywa się wydarzenie.'

    name = models.CharField(
        max_length=100, help_text=HELP_NAME, verbose_name='Nazwa')
    starts_on = models.DateField(
        help_text=HELP_STARTS_ON, verbose_name='Dzień rozpoczęcia')
    url = models.URLField(help_text=HELP_URL, verbose_name='Strona internetowa')
    town = models.CharField(
        max_length=100, help_text=HELP_TOWN, verbose_name='Miejscowość')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    def get_edit_url(self):
        return reverse('edit_external_event', kwargs=self.get_url_params())

    def get_delete_url(self):
        return reverse('delete_external_event', kwargs=self.get_url_params())

    def get_url_params(self):
        return {'pk': self.pk}

    def external_source(self):
        return True

    def location(self):
        return self.town


def get_events_for(user):
    external_events = ExternalEvent.objects.filter(starts_on__gte=date.today())
    return sorted(list(external_events), key=lambda event: event.starts_on)
