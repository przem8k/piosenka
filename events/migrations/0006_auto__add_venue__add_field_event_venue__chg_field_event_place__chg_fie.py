# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Venue'
        db.create_table('events_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='100')),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length='100', db_index=True)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length='100')),
            ('street', self.gf('django.db.models.fields.CharField')(max_length='100')),
            ('location', self.gf('events.models.LocationField')(max_length=100)),
        ))
        db.send_create_signal('events', ['Venue'])

        # Adding field 'Event.venue'
        db.add_column('events_event', 'venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Venue'], null=True), keep_default=False)

        # Changing field 'Event.place'
        db.alter_column('events_event', 'place', self.gf('django.db.models.fields.CharField')(max_length='100', null=True))

        # Changing field 'Event.address'
        db.alter_column('events_event', 'address', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Deleting model 'Venue'
        db.delete_table('events_venue')

        # Deleting field 'Event.venue'
        db.delete_column('events_event', 'venue_id')

        # Changing field 'Event.place'
        db.alter_column('events_event', 'place', self.gf('django.db.models.fields.CharField')(default='void', max_length='100'))

        # Changing field 'Event.address'
        db.alter_column('events_event', 'address', self.gf('django.db.models.fields.TextField')(default='void'))


    models = {
        'artists.artist': {
            'Meta': {'ordering': "['lastname', 'firstname']", 'object_name': 'Artist'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'void'", 'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'artists.band': {
            'Meta': {'ordering': "['name']", 'object_name': 'Band'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'events.event': {
            'Meta': {'ordering': "['datetime']", 'object_name': 'Event'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True', 'blank': 'True'}),
            'bands': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Band']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('events.models.LocationField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': "'100'", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': "'100'", 'db_index': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Venue']", 'null': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'events.venue': {
            'Meta': {'object_name': 'Venue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('events.models.LocationField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': "'100'", 'db_index': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': "'100'"})
        }
    }

    complete_apps = ['events']
