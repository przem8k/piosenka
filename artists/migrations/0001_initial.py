# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Artist'
        db.create_table('artists_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('death', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('externals', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('granted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('story', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('artists', ['Artist'])

        # Adding model 'Band'
        db.create_table('artists_band', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('externals', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('artists', ['Band'])

        # Adding M2M table for field members on 'Band'
        db.create_table('artists_band_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('band', models.ForeignKey(orm['artists.band'], null=False)),
            ('artist', models.ForeignKey(orm['artists.artist'], null=False))
        ))
        db.create_unique('artists_band_members', ['band_id', 'artist_id'])


    def backwards(self, orm):
        
        # Deleting model 'Artist'
        db.delete_table('artists_artist')

        # Deleting model 'Band'
        db.delete_table('artists_band')

        # Removing M2M table for field members on 'Band'
        db.delete_table('artists_band_members')


    models = {
        'artists.artist': {
            'Meta': {'object_name': 'Artist'},
            'birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'death': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'externals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'granted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'story': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'artists.band': {
            'Meta': {'object_name': 'Band'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'externals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['artists']
