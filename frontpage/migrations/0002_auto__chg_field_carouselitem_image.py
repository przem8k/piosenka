# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'CarouselItem.image'
        db.alter_column(u'frontpage_carouselitem', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100))


    def backwards(self, orm):
        
        # Changing field 'CarouselItem.image'
        db.alter_column(u'frontpage_carouselitem', 'image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100))


    models = {
        u'frontpage.carouselitem': {
            'Meta': {'ordering': "['position']", 'object_name': 'CarouselItem'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['frontpage']
