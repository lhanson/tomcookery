# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HRecipe'
        db.create_table('app_hrecipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('yields', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('published', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('app', ['HRecipe'])

        # Adding M2M table for field ingredients on 'HRecipe'
        db.create_table('app_hrecipe_ingredients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hrecipe', models.ForeignKey(orm['app.hrecipe'], null=False)),
            ('ingredient', models.ForeignKey(orm['app.ingredient'], null=False))
        ))
        db.create_unique('app_hrecipe_ingredients', ['hrecipe_id', 'ingredient_id'])

        # Adding M2M table for field durations on 'HRecipe'
        db.create_table('app_hrecipe_durations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hrecipe', models.ForeignKey(orm['app.hrecipe'], null=False)),
            ('duration', models.ForeignKey(orm['app.duration'], null=False))
        ))
        db.create_unique('app_hrecipe_durations', ['hrecipe_id', 'duration_id'])

        # Adding M2M table for field photos on 'HRecipe'
        db.create_table('app_hrecipe_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hrecipe', models.ForeignKey(orm['app.hrecipe'], null=False)),
            ('photo', models.ForeignKey(orm['app.photo'], null=False))
        ))
        db.create_unique('app_hrecipe_photos', ['hrecipe_id', 'photo_id'])

        # Adding M2M table for field authors on 'HRecipe'
        db.create_table('app_hrecipe_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hrecipe', models.ForeignKey(orm['app.hrecipe'], null=False)),
            ('author', models.ForeignKey(orm['app.author'], null=False))
        ))
        db.create_unique('app_hrecipe_authors', ['hrecipe_id', 'author_id'])

        # Adding M2M table for field nutrition on 'HRecipe'
        db.create_table('app_hrecipe_nutrition', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hrecipe', models.ForeignKey(orm['app.hrecipe'], null=False)),
            ('nutrition', models.ForeignKey(orm['app.nutrition'], null=False))
        ))
        db.create_unique('app_hrecipe_nutrition', ['hrecipe_id', 'nutrition_id'])

        # Adding M2M table for field tags on 'HRecipe'
        db.create_table('app_hrecipe_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hrecipe', models.ForeignKey(orm['app.hrecipe'], null=False)),
            ('tag', models.ForeignKey(orm['app.tag'], null=False))
        ))
        db.create_unique('app_hrecipe_tags', ['hrecipe_id', 'tag_id'])

        # Adding model 'Recipe'
        db.create_table('app_recipe', (
            ('hrecipe_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['app.HRecipe'], unique=True, primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('app', ['Recipe'])

        # Adding model 'Ingredient'
        db.create_table('app_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('app', ['Ingredient'])

        # Adding model 'Duration'
        db.create_table('app_duration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('app', ['Duration'])

        # Adding model 'Photo'
        db.create_table('app_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('app', ['Photo'])

        # Adding model 'Author'
        db.create_table('app_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('app', ['Author'])

        # Adding model 'Nutrition'
        db.create_table('app_nutrition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
        ))
        db.send_create_signal('app', ['Nutrition'])

        # Adding model 'Tag'
        db.create_table('app_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('app', ['Tag'])


    def backwards(self, orm):
        
        # Deleting model 'HRecipe'
        db.delete_table('app_hrecipe')

        # Removing M2M table for field ingredients on 'HRecipe'
        db.delete_table('app_hrecipe_ingredients')

        # Removing M2M table for field durations on 'HRecipe'
        db.delete_table('app_hrecipe_durations')

        # Removing M2M table for field photos on 'HRecipe'
        db.delete_table('app_hrecipe_photos')

        # Removing M2M table for field authors on 'HRecipe'
        db.delete_table('app_hrecipe_authors')

        # Removing M2M table for field nutrition on 'HRecipe'
        db.delete_table('app_hrecipe_nutrition')

        # Removing M2M table for field tags on 'HRecipe'
        db.delete_table('app_hrecipe_tags')

        # Deleting model 'Recipe'
        db.delete_table('app_recipe')

        # Deleting model 'Ingredient'
        db.delete_table('app_ingredient')

        # Deleting model 'Duration'
        db.delete_table('app_duration')

        # Deleting model 'Photo'
        db.delete_table('app_photo')

        # Deleting model 'Author'
        db.delete_table('app_author')

        # Deleting model 'Nutrition'
        db.delete_table('app_nutrition')

        # Deleting model 'Tag'
        db.delete_table('app_tag')


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
