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

        # Adding model 'Duration'
        db.create_table('app_duration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('app', ['Duration'])

        # Adding model 'Difficulty'
        db.create_table('app_difficulty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('app', ['Difficulty'])

        # Adding model 'Course'
        db.create_table('app_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('app', ['Course'])

        # Adding model 'Recipe'
        db.create_table('app_recipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('yields', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('published', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('url', self.gf('django.db.models.fields.SlugField')(default='error', max_length=50, db_index=True)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('submitor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipes_submitted', to=orm['auth.User'])),
            ('difficulty', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['app.Difficulty'], null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['app.Course'], null=True, blank=True)),
        ))
        db.send_create_signal('app', ['Recipe'])

        # Adding M2M table for field durations on 'Recipe'
        db.create_table('app_recipe_durations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['app.recipe'], null=False)),
            ('duration', models.ForeignKey(orm['app.duration'], null=False))
        ))
        db.create_unique('app_recipe_durations', ['recipe_id', 'duration_id'])

        # Adding M2M table for field photos on 'Recipe'
        db.create_table('app_recipe_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['app.recipe'], null=False)),
            ('photo', models.ForeignKey(orm['app.photo'], null=False))
        ))
        db.create_unique('app_recipe_photos', ['recipe_id', 'photo_id'])

        # Adding M2M table for field tags on 'Recipe'
        db.create_table('app_recipe_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['app.recipe'], null=False)),
            ('tag', models.ForeignKey(orm['app.tag'], null=False))
        ))
        db.create_unique('app_recipe_tags', ['recipe_id', 'tag_id'])

        # Adding M2M table for field users_voted on 'Recipe'
        db.create_table('app_recipe_users_voted', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['app.recipe'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('app_recipe_users_voted', ['recipe_id', 'user_id'])

        # Adding model 'CookoffTheme'
        db.create_table('app_cookofftheme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('winning_recipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='winning_recipe', null=True, to=orm['app.Recipe'])),
            ('runner_up_recipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_recipe', null=True, to=orm['app.Recipe'])),
            ('third_place_recipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='third_recipe', null=True, to=orm['app.Recipe'])),
            ('start_submit', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_submit', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_vote', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_vote', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('app', ['CookoffTheme'])

        # Adding M2M table for field recipes on 'CookoffTheme'
        db.create_table('app_cookofftheme_recipes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cookofftheme', models.ForeignKey(orm['app.cookofftheme'], null=False)),
            ('recipe', models.ForeignKey(orm['app.recipe'], null=False))
        ))
        db.create_unique('app_cookofftheme_recipes', ['cookofftheme_id', 'recipe_id'])

        # Adding model 'Ingredient_Measurement'
        db.create_table('app_ingredient_measurement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Ingredient'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Recipe'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('app', ['Ingredient_Measurement'])

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

        # Adding model 'ChefRank'
        db.create_table('app_chefrank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Fry Cook', max_length=15)),
        ))
        db.send_create_signal('app', ['ChefRank'])

        # Adding model 'MyProfile'
        db.create_table('app_myprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('recipePoints', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('commentPoints', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('votePoints', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('recipeLiked', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True)),
            ('websiteName', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('chefRank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.ChefRank'], null=True, blank=True)),
        ))
        db.send_create_signal('app', ['MyProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Ingredient'
        db.delete_table('app_ingredient')

        # Deleting model 'Duration'
        db.delete_table('app_duration')

        # Deleting model 'Difficulty'
        db.delete_table('app_difficulty')

        # Deleting model 'Course'
        db.delete_table('app_course')

        # Deleting model 'Recipe'
        db.delete_table('app_recipe')

        # Removing M2M table for field durations on 'Recipe'
        db.delete_table('app_recipe_durations')

        # Removing M2M table for field photos on 'Recipe'
        db.delete_table('app_recipe_photos')

        # Removing M2M table for field tags on 'Recipe'
        db.delete_table('app_recipe_tags')

        # Removing M2M table for field users_voted on 'Recipe'
        db.delete_table('app_recipe_users_voted')

        # Deleting model 'CookoffTheme'
        db.delete_table('app_cookofftheme')

        # Removing M2M table for field recipes on 'CookoffTheme'
        db.delete_table('app_cookofftheme_recipes')

        # Deleting model 'Ingredient_Measurement'
        db.delete_table('app_ingredient_measurement')

        # Deleting model 'Photo'
        db.delete_table('app_photo')

        # Deleting model 'Tag'
        db.delete_table('app_tag')

        # Deleting model 'ChefRank'
        db.delete_table('app_chefrank')

        # Deleting model 'MyProfile'
        db.delete_table('app_myprofile')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'recipes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'all_recipes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['app.Recipe']"}),
            'runner_up_recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_recipe'", 'null': 'True', 'to': "orm['app.Recipe']"}),
            'start_submit': ('django.db.models.fields.DateTimeField', [], {}),
            'start_vote': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {}),
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
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
            'users_voted': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recipe_votes'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
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
