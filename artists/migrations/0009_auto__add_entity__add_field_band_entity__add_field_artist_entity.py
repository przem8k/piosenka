# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Entity'
        db.create_table('artists_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('still_plays', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('website', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200, null=True)),
            ('kind', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('is_band', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('artists', ['Entity'])

        # Adding field 'Band.entity'
        db.add_column('artists_band', 'entity',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['artists.Entity'], null=True),
                      keep_default=False)

        # Adding field 'Artist.entity'
        db.add_column('artists_artist', 'entity',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['artists.Entity'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Entity'
        db.delete_table('artists_entity')

        # Deleting field 'Band.entity'
        db.delete_column('artists_band', 'entity_id')

        # Deleting field 'Artist.entity'
        db.delete_column('artists_artist', 'entity_id')


    models = {
        'artists.artist': {
            'Meta': {'object_name': 'Artist', 'ordering': "['lastname', 'firstname']"},
            'display': ('django.db.models.fields.BooleanField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['artists.Entity']", 'null': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'default': "'void'", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        },
        'artists.band': {
            'Meta': {'object_name': 'Band', 'ordering': "['name']"},
            'display': ('django.db.models.fields.BooleanField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['artists.Entity']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        },
        'artists.entity': {
            'Meta': {'object_name': 'Entity', 'ordering': "['is_band', 'name', 'first_name']"},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_band': ('django.db.models.fields.BooleanField', [], {}),
            'kind': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'}),
            'still_plays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['artists']