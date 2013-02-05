# -*- coding: utf-8 -*-
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

miesiace = {
    '01': u'stycznia',
    '02': u'lutego',
    '03': u'marca',
    '04': u'kwietnia',
    '05': u'maja',
    '06': u'czerwca',
    '07': u'lipca',
    '08': u'sierpnia',
    '09': u'września',
    '10': u'paźdzernika',
    '11': u'listopada',
    '12': u'grudnia'
}

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

    @models.permalink
    def get_absolute_url(self):
        return('venue', (), {
            'slug': self.slug,
        })

    def location_lat(self):
        a, b = self.location.split(',')
        return float(a)
    def location_lng(self):
        a, b = self.location.split(',')
        return float(b)

    def save(self, *args, **kwargs):
        if not self.location:
            from googlemaps import GoogleMaps
            from unidecode import unidecode
            address = self.street + ', ' + self.town;
            ascii_address = unidecode(unicode(address))
            gmaps = GoogleMaps(settings.GOOGLE_MAPS_API_KEY)
            lat, lng = gmaps.address_to_latlng(ascii_address)
            self.location = str(lat) + ',' + str(lng)
        super(Venue, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s - %s" % (self.town, self.name)
    class Meta:
        ordering = ["town", "name"]    

class Event(models.Model):
    name = models.CharField(max_length="100")	
    slug = models.SlugField(max_length="100", unique_for_date="datetime")
    datetime = models.DateTimeField()
    price = models.CharField(max_length="100", help_text="E.g. 5zl, wstep wolny, etc.", null=True)
    artists = models.ManyToManyField(Artist, null=True,blank=True)
    bands = models.ManyToManyField(Band, null=True,blank=True)
    description = models.TextField()
    website = models.URLField(blank=True,null=True)
    venue = models.ForeignKey(Venue, null=False, blank=False)
    
    objects = models.Manager()
    current = CurrentEventManager()
    past = PastEventManager()
    
    def location_lat(self):
        return self.venue.location_lat()
    def location_lng(self):
        return self.venue.location_lng()
    def date(self):
        return "%s.%s" % (self.datetime.strftime("%e"),self.datetime.strftime("%m"))
    @models.permalink
    def get_absolute_url(self):
        return ('event', (), { 
            'year': self.datetime.strftime("%Y"),
            'month': self.datetime.strftime("%m"),
            'day': self.datetime.strftime("%d"),
            'slug': self.slug
        })                      
    def __unicode__(self):
        return "%s - %s (%s)" % (self.date(), self.name,self.venue.town)
    class Meta:
        ordering = ["datetime"]
