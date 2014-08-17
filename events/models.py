from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from artists.models import Entity
from frontpage.render import render_trevor

from markdown import markdown


class CurrentEventManager(models.Manager):
    def get_query_set(self):
        return super(CurrentEventManager, self).get_query_set().filter(datetime__gte=datetime.now())


class PastEventManager(models.Manager):
    def get_query_set(self):
        return super(PastEventManager, self).get_query_set().filter(datetime__lt=datetime.now())


class Venue(models.Model):
    name = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    lat = models.FloatField(editable=False, help_text="Latitude.")
    lon = models.FloatField(editable=False, help_text="Longtitude.")

    class Meta:
        ordering = ["town", "name"]

    def __str__(self):
        return "%s - %s" % (self.town, self.name)

    def clean(self):
        super(Venue, self).clean()
        from pygeocoder import Geocoder
        from pygeolib import GeocoderError
        address = str(self.street) + ', ' + str(self.town)
        try:
            geo = Geocoder.geocode(address)
        except GeocoderError:
            raise ValidationError("Geo lookup fails to recognize this address.")
        self.lat, self.lon = geo[0].coordinates

    @models.permalink
    def get_absolute_url(self):
        return('venue_detail', (), {
            'slug': self.slug,
        })


class PublishedEventManager(models.Manager):
    def get_queryset(self):
        return super(PublishedEventManager, self).get_queryset().filter(published=True)


class Event(models.Model):
    objects = models.Manager()
    po = PublishedEventManager()

    name = models.CharField(max_length=100,
                            help_text="Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego' "
                                      "lub 'V Festiwal Piosenki Wymyślnej w Katowicach'.")
    slug = models.SlugField(max_length=100, unique_for_date="datetime")
    datetime = models.DateTimeField()
    price = models.CharField(max_length=100, null=True, blank=True,
                             help_text="E.g. 20zł, wstęp wolny. W przypadku braku danych pozostaw "
                                       "puste.")
    description_html = models.TextField(null=True, blank=True, editable=False)
    description_trevor = models.TextField()
    website = models.URLField(null=True, blank=True,
                              help_text="Strona internetowa wydarzenia, źródło informacji. "
                                        "W przypadku braku danych pozostaw puste.")
    venue = models.ForeignKey(Venue, null=False, blank=False)
    published = models.BooleanField(default=True, help_text="Only admins see not-published songs")
    author = models.ForeignKey(User, editable=False)
    pub_date = models.DateTimeField(editable=False)

    objects = models.Manager()
    current = CurrentEventManager()
    past = PastEventManager()

    class Meta:
        ordering = ["datetime"]

    def __str__(self):
        return "%s - %s (%s)" % (self.datetime.strftime("%d.%m.%Y"), self.name, self.venue.town)

    def save(self, *args, **kwargs):
        self.description_html = render_trevor(self.description_trevor)
        if not self.pub_date:
            self.pub_date = datetime.now()
        super(Event, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('event_detail', (), {
            'year': self.datetime.strftime("%Y"),
            'month': self.datetime.strftime("%m"),
            'day': self.datetime.strftime("%d"),
            'slug': self.slug
        })

    @models.permalink
    def get_edit_url(self):
        return ('edit_event', (), {
            'year': self.datetime.strftime("%Y"),
            'month': self.datetime.strftime("%m"),
            'day': self.datetime.strftime("%d"),
            'slug': self.slug
        })

    def lat(self):
        return self.venue.lat

    def lon(self):
        return self.venue.lon

    def performers(self):
        return [x.entity for x in EntityPerformance.objects.filter(event=self)]


class EntityPerformance(models.Model):
    event = models.ForeignKey(Event)
    entity = models.ForeignKey(Entity)
