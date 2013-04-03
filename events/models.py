# -*- coding: utf-8 -*-
from markdown import markdown
from datetime import datetime
from django.db import models
from django.conf import settings
from artists.models import Artist, Band
from events.forms import LocationFormField
from events.widgets import LocationWidget

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^events.models.LocationField"])

class LocationField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super(LocationField, self).__init__(*args, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults['widget'] = LocationWidget
        return super(LocationField, self).formfield(**defaults)


class CurrentEventManager(models.Manager):
    def get_query_set(self):
        return super(CurrentEventManager, self).get_query_set().filter(datetime__gte=datetime.now())
        

class PastEventManager(models.Manager):
    def get_query_set(self):
        return super(PastEventManager, self).get_query_set().filter(datetime__lt=datetime.now())


class Venue(models.Model):
    name = models.CharField(max_length="100")
    town = models.CharField(max_length="100")
    street = models.CharField(max_length="100")
    slug = models.SlugField(max_length="100", unique=True)
    location = LocationField(editable=False)

    class Meta:
        ordering = ["town", "name"]    

    def __unicode__(self):
        return "%s - %s" % (self.town, self.name)

    def save(self, *args, **kwargs):
        from pygeocoder import Geocoder
        from unidecode import unidecode
        address = self.street + ', ' + self.town;
        ascii_address = unidecode(unicode(address))
        geo = Geocoder.geocode(ascii_address)
        if len(geo) == 0:
            raise RuntimeError("Address geo lookup failed.")
        lat, lng = geo[0].coordinates
        self.location = str(lat) + ',' + str(lng)
        super(Venue, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return('venue_detail', (), {
            'slug': self.slug,
        })

    def location_lat(self):
        a, b = self.location.split(',')
        return float(a)

    def location_lng(self):
        a, b = self.location.split(',')
        return float(b)


class Event(models.Model):
    name = models.CharField(max_length="100")	
    slug = models.SlugField(max_length="100", unique_for_date="datetime")
    datetime = models.DateTimeField()
    price = models.CharField(max_length="100", null=True, blank=True, help_text="E.g. 5zl, wstep wolny, brak danych, etc.")
    artists = models.ManyToManyField(Artist, null=True, blank=True)
    bands = models.ManyToManyField(Band, null=True, blank=True)
    description = models.TextField(null=True, blank=True, help_text="Event description, written in Markdown.")
    description_html = models.TextField(null=True, blank=True, editable=False)
    website = models.URLField(null=True, blank=True)
    venue = models.ForeignKey(Venue, null=False, blank=False)
    
    objects = models.Manager()
    current = CurrentEventManager()
    past = PastEventManager()
    
    class Meta:
        ordering = ["datetime"]

    def __unicode__(self):
        return "%s - %s (%s)" % (self.date(), self.name, self.venue.town)

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description, safe_mode='escape')
        super(Event, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('event_detail', (), { 
            'year': self.datetime.strftime("%Y"),
            'month': self.datetime.strftime("%m"),
            'day': self.datetime.strftime("%d"),
            'slug': self.slug
        })                      

    def location_lat(self):
        return self.venue.location_lat()

    def location_lng(self):
        return self.venue.location_lng()

    def date(self):
        return "%s.%s" % (self.datetime.strftime("%e"),self.datetime.strftime("%m"))
