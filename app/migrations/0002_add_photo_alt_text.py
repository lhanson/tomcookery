# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Photo.alt_text'
        db.add_column('app_photo', 'alt_text', self.gf('django.db.models.fields.CharField')(default='', max_length=40), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Photo.alt_text'
        db.delete_column('app_photo', 'alt_text')


    models = {
        'app.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'app.duration': {
            'Meta': {'object_name': 'Duration'},
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.hrecipe': {
            'Meta': {'object_name': 'HRecipe'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Author']", 'symmetrical': 'False', 'blank': 'True'}),
            'durations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Duration']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Ingredient']", 'symmetrical': 'False'}),
            'instructions': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'nutrition': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Nutrition']", 'symmetrical': 'False', 'blank': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Photo']", 'symmetrical': 'False', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'yields': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'app.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'app.nutrition': {
            'Meta': {'object_name': 'Nutrition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'app.photo': {
            'Meta': {'object_name': 'Photo'},
            'alt_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'app.recipe': {
            'Meta': {'object_name': 'Recipe', '_ormbases': ['app.HRecipe']},
            'hrecipe_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app.HRecipe']", 'unique': 'True', 'primary_key': 'True'}),
            'submitter': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'app.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['app']
