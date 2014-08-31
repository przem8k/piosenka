# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Venue.town'
        db.alter_column(u'events_venue', 'town', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Venue.name'
        db.alter_column(u'events_venue', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Venue.street'
        db.alter_column(u'events_venue', 'street', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Venue.slug'
        db.alter_column(u'events_venue', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100))

        # Changing field 'Event.slug'
        db.alter_column(u'events_event', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100))

        # Changing field 'Event.price'
        db.alter_column(u'events_event', 'price', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Event.name'
        db.alter_column(u'events_event', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))


    def backwards(self, orm):
        
        # Changing field 'Venue.town'
        db.alter_column(u'events_venue', 'town', self.gf('django.db.models.fields.CharField')(max_length='100'))

        # Changing field 'Venue.name'
        db.alter_column(u'events_venue', 'name', self.gf('django.db.models.fields.CharField')(max_length='100'))

        # Changing field 'Venue.street'
        db.alter_column(u'events_venue', 'street', self.gf('django.db.models.fields.CharField')(max_length='100'))

        # Changing field 'Venue.slug'
        db.alter_column(u'events_venue', 'slug', self.gf('django.db.models.fields.SlugField')(max_length='100', unique=True))

        # Changing field 'Event.slug'
        db.alter_column(u'events_event', 'slug', self.gf('django.db.models.fields.SlugField')(max_length='100'))

        # Changing field 'Event.price'
        db.alter_column(u'events_event', 'price', self.gf('django.db.models.fields.CharField')(max_length='100', null=True))

        # Changing field 'Event.name'
        db.alter_column(u'events_event', 'name', self.gf('django.db.models.fields.CharField')(max_length='100'))


    models = {
        u'artists.artist': {
            'Meta': {'ordering': "['lastname', 'firstname']", 'object_name': 'Artist'},
            'display': ('django.db.models.fields.BooleanField', [], {}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'void'", 'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'artists.band': {
            'Meta': {'ordering': "['name']", 'object_name': 'Band'},
            'display': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['artists.Artist']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'events.event': {
            'Meta': {'ordering': "['datetime']", 'object_name': 'Event'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['artists.Artist']", 'null': 'True', 'blank': 'True'}),
            'bands': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['artists.Band']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Venue']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'events.venue': {
            'Meta': {'ordering': "['town', 'name']", 'object_name': 'Venue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('events.models.LocationField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['events']
