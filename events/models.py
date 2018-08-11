from datetime import timedelta
import uuid

from django import urls
from django.db import models
from django.utils import timezone
from django.urls import reverse

from pygeocoder import Geocoder
from pygeolib import GeocoderError

from base.overrides import overrides
from content import url_scheme
from content.models import ContentItem
from content.slug import SlugLogicMixin, SlugFieldMixin
from content.trevor import render_trevor, put_text_in_trevor


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


class Venue(SlugFieldMixin, models.Model):
    name = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    lat = models.FloatField(null=True, editable=False, help_text='Latitude.')
    lon = models.FloatField(null=True, editable=False, help_text='Longtitude.')

    @staticmethod
    def create_for_testing():
        venue = Venue()
        venue.name = str(uuid.uuid4()).replace('-', '')
        venue.town = 'New York'
        venue.street = '233 Madison Avenue'
        venue.lat = 0.0
        venue.lon = 0.0
        venue.full_clean()
        venue.save()
        return venue

    class Meta:
        ordering = ['town', 'name']

    def __str__(self):
        return '%s - %s' % (self.town, self.name)

    def clean(self):
        super().clean()
        address = str(self.street) + ', ' + str(self.town)
        try:
            geo = Geocoder.geocode(address)
            self.lat, self.lon = geo[0].coordinates
        except GeocoderError:
            # Geo lookup failed to recognize this address.
            pass

    def get_absolute_url(self):
        return urls.reverse('venue_detail', kwargs={'slug': self.slug})

    @overrides(SlugFieldMixin)
    def get_slug_elements(self):
        assert self.name
        assert self.town
        return [self.name, self.town]


class Event(SlugLogicMixin, url_scheme.ViewEditReviewApprove, ContentItem):
    HELP_NAME = """Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego'
lub 'V Festiwal Piosenki Wymyślnej w Katowicach'."""
    HELP_PRICE = """Np. 20zł, wstęp wolny. W przypadku braku danych pozostaw
puste."""
    HELP_WEBSITE = """Strona internetowa wydarzenia, źródło informacji. W
przypadku braku danych pozostaw puste."""

    name = models.CharField(max_length=100, help_text=HELP_NAME)
    datetime = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    description_trevor = models.TextField()
    price = models.CharField(
        max_length=100, null=True, blank=True, help_text=HELP_PRICE)
    website = models.URLField(null=True, blank=True, help_text=HELP_WEBSITE)

    slug = models.SlugField(
        max_length=100, unique_for_date='datetime', editable=False)
    description_html = models.TextField(editable=False)

    @staticmethod
    def create_for_testing(author, venue=None):
        event = Event()
        event.author = author
        event.name = str(uuid.uuid4()).replace('-', '')
        event.description_trevor = put_text_in_trevor('Abc')
        event.datetime = timezone.now() + timedelta(days=365)
        event.venue = venue if venue else Venue.create_for_testing()
        event.full_clean()
        event.save()
        return event

    class Meta(ContentItem.Meta):
        ordering = ['datetime']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = render_trevor(self.description_trevor)
        super().save(*args, **kwargs)

    def get_url_params(self):
        return {
            'year': self.datetime.strftime('%Y'),
            'month': self.datetime.strftime('%m'),
            'day': self.datetime.strftime('%d'),
            'slug': self.slug
        }

    @overrides(SlugLogicMixin)
    def get_slug_elements(self):
        return [self.name, self.venue.town]

    @overrides(url_scheme.ViewEditReviewApprove)
    def get_url_name(self):
        return 'event'

    def lat(self):
        return self.venue.lat

    def lon(self):
        return self.venue.lon

    def location(self):
        return self.venue.town

    def sort_order_time(self):
        return self.datetime


class FbEvent(models.Model):
    fb_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    town = models.CharField(max_length=100, null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return 'https://www.facebook.com/events/%s/' % (self.fb_id)

    def external_source(self):
        return 'fb'

    def location(self):
        return self.town

    def sort_order_time(self):
        return self.datetime


class ExternalEvent(models.Model):
    HELP_NAME = 'Nazwa wydarzenia, w tym występujący artysta lub zespół.'
    HELP_STARTS_AT = 'Data i godzina rozpoczęcia wydarzenia.'
    HELP_URL = 'Strona internetowa wydarzenia (może być na Facebooku).'
    HELP_TOWN = 'Miejscowość w którym odbywa się wydarzenie.'

    name = models.CharField(max_length=100, help_text=HELP_NAME,
                            verbose_name='Nazwa')
    starts_at = models.DateTimeField(blank=True, null=False,
                                     help_text=HELP_STARTS_AT,
                                     verbose_name='Czas rozpoczęcia')
    url = models.URLField(help_text=HELP_URL, verbose_name='Strona internetowa')
    town = models.CharField(max_length=100, help_text=HELP_TOWN,
                            verbose_name='Miejscowość')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    def get_edit_url(self):
        return reverse(
            'edit_external_event', kwargs=self.get_url_params())

    def get_delete_url(self):
        return reverse(
            'delete_external_event', kwargs=self.get_url_params())

    def get_url_params(self):
        return {
            'pk': self.pk
        }

    def external_source(self):
        return True

    def location(self):
        return self.town

    def sort_order_time(self):
        return self.starts_at


def get_events_for(user):
    site_events = Event.items_visible_to(user).filter(
        datetime__gte=timezone.now())
    fb_events = FbEvent.objects.filter(datetime__gte=timezone.now())
    external_events = ExternalEvent.objects.filter(
        starts_at__gte=timezone.now())
    return sorted(
        list(site_events) + list(fb_events) + list(external_events),
        key=lambda event: event.sort_order_time())
