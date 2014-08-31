# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Artist.description'
        db.delete_column('artists_artist', 'description')

        # Deleting field 'Artist.birth'
        db.delete_column('artists_artist', 'birth')

        # Deleting field 'Artist.story'
        db.delete_column('artists_artist', 'story')

        # Deleting field 'Artist.death'
        db.delete_column('artists_artist', 'death')

        # Deleting field 'Artist.granted'
        db.delete_column('artists_artist', 'granted')

        # Deleting field 'Artist.externals'
        db.delete_column('artists_artist', 'externals')

        # Changing field 'Artist.slug'
        db.alter_column('artists_artist', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100))

        # Adding unique constraint on 'Artist', fields ['slug']
        db.create_unique('artists_artist', ['slug'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Artist', fields ['slug']
        db.delete_unique('artists_artist', ['slug'])

        # Adding field 'Artist.description'
        db.add_column('artists_artist', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Artist.birth'
        db.add_column('artists_artist', 'birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Artist.story'
        db.add_column('artists_artist', 'story', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Artist.death'
        db.add_column('artists_artist', 'death', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Artist.granted'
        db.add_column('artists_artist', 'granted', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Artist.externals'
        db.add_column('artists_artist', 'externals', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Changing field 'Artist.slug'
        db.alter_column('artists_artist', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True))


    models = {
        'artists.artist': {
            'Meta': {'ordering': "['lastname', 'firstname']", 'object_name': 'Artist'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'void'", 'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'artists.band': {
            'Meta': {'ordering': "['name']", 'object_name': 'Band'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'externals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['artists']
