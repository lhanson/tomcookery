# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Ingredient'
        db.create_table('app_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('app', ['Ingredient'])

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
            ('url', self.gf('django.db.models.fields.SlugField')(default='error', max_length=50, db_index=True)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('submitor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipes_submitted', to=orm['auth.User'])),
        ))
        db.send_create_signal('app', ['Recipe'])

        # Adding M2M table for field users_voted on 'Recipe'
        db.create_table('app_recipe_users_voted', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['app.recipe'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('app_recipe_users_voted', ['recipe_id', 'user_id'])

        # Adding model 'Ingredient_Measurement'
        db.create_table('app_ingredient_measurement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Ingredient'])),
            ('hrecipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.HRecipe'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('app', ['Ingredient_Measurement'])

        # Adding model 'Duration'
        db.create_table('app_duration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('app', ['Duration'])

        # Adding model 'Photo'
        db.create_table('app_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alt_text', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('app', ['Photo'])

        # Adding model 'Tag'
        db.create_table('app_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('app', ['Tag'])


    def backwards(self, orm):
        
        # Deleting model 'Ingredient'
        db.delete_table('app_ingredient')

        # Deleting model 'HRecipe'
        db.delete_table('app_hrecipe')

        # Removing M2M table for field durations on 'HRecipe'
        db.delete_table('app_hrecipe_durations')

        # Removing M2M table for field photos on 'HRecipe'
        db.delete_table('app_hrecipe_photos')

        # Removing M2M table for field tags on 'HRecipe'
        db.delete_table('app_hrecipe_tags')

        # Deleting model 'Recipe'
        db.delete_table('app_recipe')

        # Removing M2M table for field users_voted on 'Recipe'
        db.delete_table('app_recipe_users_voted')

        # Deleting model 'Ingredient_Measurement'
        db.delete_table('app_ingredient_measurement')

        # Deleting model 'Duration'
        db.delete_table('app_duration')

        # Deleting model 'Photo'
        db.delete_table('app_photo')

        # Deleting model 'Tag'
        db.delete_table('app_tag')


    models = {
        'app.duration': {
            'Meta': {'object_name': 'Duration'},
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.hrecipe': {
            'Meta': {'object_name': 'HRecipe'},
            'durations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Duration']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Ingredient']", 'through': "orm['app.Ingredient_Measurement']", 'symmetrical': 'False'}),
            'instructions': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Photo']", 'symmetrical': 'False', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'yields': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'app.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'app.ingredient_measurement': {
            'Meta': {'object_name': 'Ingredient_Measurement'},
            'hrecipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.HRecipe']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Ingredient']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
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
            'submitor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipes_submitted'", 'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.SlugField', [], {'default': "'error'", 'max_length': '50', 'db_index': 'True'}),
            'users_voted': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recipe_votes'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'app.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
        }
    }

    complete_apps = ['app']
