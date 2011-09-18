# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Recipe.votes_ing'
        db.add_column('app_recipe', 'votes_ing', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Recipe.votes_theme'
        db.add_column('app_recipe', 'votes_theme', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Recipe.votes_custom'
        db.add_column('app_recipe', 'votes_custom', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Removing M2M table for field users_voted on 'Recipe'
        db.delete_table('app_recipe_users_voted')

        # Adding M2M table for field users_voted_ing on 'MyProfile'
        db.create_table('app_myprofile_users_voted_ing', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myprofile', models.ForeignKey(orm['app.myprofile'], null=False)),
            ('cookofftheme', models.ForeignKey(orm['app.cookofftheme'], null=False))
        ))
        db.create_unique('app_myprofile_users_voted_ing', ['myprofile_id', 'cookofftheme_id'])

        # Adding M2M table for field users_voted_theme on 'MyProfile'
        db.create_table('app_myprofile_users_voted_theme', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myprofile', models.ForeignKey(orm['app.myprofile'], null=False)),
            ('cookofftheme', models.ForeignKey(orm['app.cookofftheme'], null=False))
        ))
        db.create_unique('app_myprofile_users_voted_theme', ['myprofile_id', 'cookofftheme_id'])

        # Adding M2M table for field users_voted_overall on 'MyProfile'
        db.create_table('app_myprofile_users_voted_overall', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myprofile', models.ForeignKey(orm['app.myprofile'], null=False)),
            ('cookofftheme', models.ForeignKey(orm['app.cookofftheme'], null=False))
        ))
        db.create_unique('app_myprofile_users_voted_overall', ['myprofile_id', 'cookofftheme_id'])


    def backwards(self, orm):
        
        # Deleting field 'Recipe.votes_ing'
        db.delete_column('app_recipe', 'votes_ing')

        # Deleting field 'Recipe.votes_theme'
        db.delete_column('app_recipe', 'votes_theme')

        # Deleting field 'Recipe.votes_custom'
        db.delete_column('app_recipe', 'votes_custom')

        # Adding M2M table for field users_voted on 'Recipe'
        db.create_table('app_recipe_users_voted', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['app.recipe'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('app_recipe_users_voted', ['recipe_id', 'user_id'])

        # Removing M2M table for field users_voted_ing on 'MyProfile'
        db.delete_table('app_myprofile_users_voted_ing')

        # Removing M2M table for field users_voted_theme on 'MyProfile'
        db.delete_table('app_myprofile_users_voted_theme')

        # Removing M2M table for field users_voted_overall on 'MyProfile'
        db.delete_table('app_myprofile_users_voted_overall')


    models = {
        'app.chefrank': {
            'Meta': {'object_name': 'ChefRank'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Fry Cook'", 'max_length': '15'})
        },
        'app.cookofftheme': {
            'Meta': {'object_name': 'CookoffTheme'},
            'end_submit': ('django.db.models.fields.DateTimeField', [], {}),
            'end_vote': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Ingredient']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Photo']", 'symmetrical': 'False', 'blank': 'True'}),
            'recipes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'all_recipes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['app.Recipe']"}),
            'runner_up_recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_recipe'", 'null': 'True', 'to': "orm['app.Recipe']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'start_submit': ('django.db.models.fields.DateTimeField', [], {}),
            'start_vote': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'third_place_recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_recipe'", 'null': 'True', 'to': "orm['app.Recipe']"}),
            'winning_recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'winning_recipe'", 'null': 'True', 'to': "orm['app.Recipe']"})
        },
        'app.course': {
            'Meta': {'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'app.difficulty': {
            'Meta': {'object_name': 'Difficulty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'app.duration': {
            'Meta': {'object_name': 'Duration'},
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'app.ingredient_measurement': {
            'Meta': {'object_name': 'Ingredient_Measurement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Ingredient']"}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Recipe']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'app.myprofile': {
            'Meta': {'object_name': 'MyProfile'},
            'chefRank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.ChefRank']", 'null': 'True', 'blank': 'True'}),
            'commentPoints': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipeLiked': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recipePoints': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'twitterHandle': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'users_voted_ing': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recipe_votes_ing'", 'symmetrical': 'False', 'to': "orm['app.CookoffTheme']"}),
            'users_voted_overall': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recipe_votes_overall'", 'symmetrical': 'False', 'to': "orm['app.CookoffTheme']"}),
            'users_voted_theme': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recipe_votes_theme'", 'symmetrical': 'False', 'to': "orm['app.CookoffTheme']"}),
            'votePoints': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'websiteName': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'app.photo': {
            'Meta': {'object_name': 'Photo'},
            'alt_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'app.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['app.Course']", 'null': 'True', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['app.Difficulty']", 'null': 'True', 'blank': 'True'}),
            'durations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Duration']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Ingredient']", 'through': "orm['app.Ingredient_Measurement']", 'symmetrical': 'False'}),
            'instructions': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Photo']", 'symmetrical': 'False', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'submitor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipes_submitted'", 'to': "orm['auth.User']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'url': ('django.db.models.fields.SlugField', [], {'default': "'error'", 'max_length': '50', 'db_index': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'votes_custom': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'votes_ing': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'votes_theme': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'yields': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
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
