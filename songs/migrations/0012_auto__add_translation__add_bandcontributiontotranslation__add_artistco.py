# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Translation'
        db.create_table('songs_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['songs.Song'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link_youtube', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('link_wrzuta', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('score1', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('score2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('score3', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('capo_fret', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lyrics', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('songs', ['Translation'])

        # Adding model 'BandContributionToTranslation'
        db.create_table('songs_bandcontributiontotranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['songs.Translation'])),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['artists.Band'])),
            ('performed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('songs', ['BandContributionToTranslation'])

        # Adding model 'ArtistContributionToTranslation'
        db.create_table('songs_artistcontributiontotranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('translation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['songs.Translation'])),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['artists.Artist'])),
            ('performed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('translated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('songs', ['ArtistContributionToTranslation'])


    def backwards(self, orm):
        
        # Deleting model 'Translation'
        db.delete_table('songs_translation')

        # Deleting model 'BandContributionToTranslation'
        db.delete_table('songs_bandcontributiontotranslation')

        # Deleting model 'ArtistContributionToTranslation'
        db.delete_table('songs_artistcontributiontotranslation')


    models = {
        'artists.artist': {
            'Meta': {'ordering': "['lastname', 'firstname']", 'object_name': 'Artist'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 1, 0, 50, 20, 829902)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 1, 0, 50, 20, 829807)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'songs.artistcontribution': {
            'Meta': {'object_name': 'ArtistContribution'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Artist']"}),
            'composed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Song']"}),
            'texted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'translated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'songs.artistcontributiontotranslation': {
            'Meta': {'object_name': 'ArtistContributionToTranslation'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'translated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Translation']"})
        },
        'songs.bandcontribution': {
            'Meta': {'object_name': 'BandContribution'},
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Band']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Song']"})
        },
        'songs.bandcontributiontotranslation': {
            'Meta': {'object_name': 'BandContributionToTranslation'},
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Band']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Translation']"})
        },
        'songs.song': {
            'Meta': {'ordering': "['title']", 'object_name': 'Song'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True', 'through': "orm['songs.ArtistContribution']", 'blank': 'True'}),
            'bands': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Band']", 'null': 'True', 'through': "orm['songs.BandContribution']", 'blank': 'True'}),
            'capo_fret': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'disambig': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'link_wrzuta': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_youtube': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'original_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'score2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'score3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'songs.translation': {
            'Meta': {'ordering': "['title']", 'object_name': 'Translation'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True', 'through': "orm['songs.ArtistContributionToTranslation']", 'blank': 'True'}),
            'bands': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Band']", 'null': 'True', 'through': "orm['songs.BandContributionToTranslation']", 'blank': 'True'}),
            'capo_fret': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_wrzuta': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_youtube': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'original_song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Song']"}),
            'score1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'score2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'score3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'songs.usercategory': {
            'Meta': {'object_name': 'UserCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'songs.usersubscription': {
            'Meta': {'object_name': 'UserSubscription'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.UserCategory']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['songs.Song']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['songs']
