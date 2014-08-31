# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Band'
        db.delete_table('artists_band')

        # Removing M2M table for field members on 'Band'
        db.delete_table(db.shorten_name('artists_band_members'))

        # Deleting model 'Artist'
        db.delete_table('artists_artist')


    def backwards(self, orm):
        # Adding model 'Band'
        db.create_table('artists_band', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['artists.Entity'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('website', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200, null=True)),
            ('display', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('artists', ['Band'])

        # Adding M2M table for field members on 'Band'
        m2m_table_name = db.shorten_name('artists_band_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('band', models.ForeignKey(orm['artists.band'], null=False)),
            ('artist', models.ForeignKey(orm['artists.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['band_id', 'artist_id'])

        # Adding model 'Artist'
        db.create_table('artists_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, default='void')),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['artists.Entity'], null=True)),
            ('website', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200, null=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('kind', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('display', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('artists', ['Artist'])


    models = {
        'artists.entity': {
            'Meta': {'object_name': 'Entity', 'ordering': "['is_band', 'name', 'first_name']"},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_band': ('django.db.models.fields.BooleanField', [], {}),
            'kind': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'still_plays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['artists']