# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ArtistContribution.entity_contribution'
        db.add_column('songs_artistcontribution', 'entity_contribution',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['songs.EntityContribution'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'BandContribution.entity_contribution'
        db.add_column('songs_bandcontribution', 'entity_contribution',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['songs.EntityContribution'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ArtistContribution.entity_contribution'
        db.delete_column('songs_artistcontribution', 'entity_contribution_id')

        # Deleting field 'BandContribution.entity_contribution'
        db.delete_column('songs_bandcontribution', 'entity_contribution_id')


    models = {
        'artists.artist': {
            'Meta': {'object_name': 'Artist', 'ordering': "['lastname', 'firstname']"},
            'display': ('django.db.models.fields.BooleanField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Entity']", 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'default': "'void'"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'artists.band': {
            'Meta': {'object_name': 'Band', 'ordering': "['name']"},
            'display': ('django.db.models.fields.BooleanField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Entity']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['artists.Artist']", 'null': 'True', 'blank': 'True', 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'artists.entity': {
            'Meta': {'object_name': 'Entity', 'ordering': "['is_band', 'name', 'first_name']"},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_band': ('django.db.models.fields.BooleanField', [], {}),
            'kind': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'}),
            'still_plays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'songs.artistcontribution': {
            'Meta': {'object_name': 'ArtistContribution'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Artist']"}),
            'composed': ('django.db.models.fields.BooleanField', [], {}),
            'entity_contribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.EntityContribution']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed': ('django.db.models.fields.BooleanField', [], {}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Song']"}),
            'texted': ('django.db.models.fields.BooleanField', [], {}),
            'translated': ('django.db.models.fields.BooleanField', [], {})
        },
        'songs.bandcontribution': {
            'Meta': {'object_name': 'BandContribution'},
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Band']"}),
            'entity_contribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.EntityContribution']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed': ('django.db.models.fields.BooleanField', [], {}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Song']"})
        },
        'songs.entitycontribution': {
            'Meta': {'object_name': 'EntityContribution'},
            'composed': ('django.db.models.fields.BooleanField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed': ('django.db.models.fields.BooleanField', [], {}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Song']"}),
            'texted': ('django.db.models.fields.BooleanField', [], {}),
            'translated': ('django.db.models.fields.BooleanField', [], {})
        },
        'songs.song': {
            'Meta': {'object_name': 'Song', 'ordering': "['title', 'disambig']"},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['songs.ArtistContribution']", 'to': "orm['artists.Artist']", 'null': 'True', 'blank': 'True', 'symmetrical': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'bands': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['songs.BandContribution']", 'to': "orm['artists.Band']", 'null': 'True', 'blank': 'True', 'symmetrical': 'False'}),
            'capo_fret': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'disambig': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'has_extra_chords': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'link_wrzuta': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_youtube': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'original_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_songs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['songs.Song']", 'related_name': "'related_songs_rel_+'", 'null': 'True', 'blank': 'True'}),
            'score1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'score2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'score3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['songs']