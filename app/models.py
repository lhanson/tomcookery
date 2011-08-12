from django.db import models
from django.contrib.auth.models import User
import os

class Ingredient(models.Model):
    """ A single ingredient """
    name = models.CharField(max_length=20)
    def __unicode__(self):
    	return self.name
    

class Recipe(models.Model):
	""" Representation of an hrecipe-based recipe (see http://microformats.org/wiki/hrecipe) """
	name = models.CharField(max_length=40) # hrecipe field name is "fn"
	ingredients = models.ManyToManyField('Ingredient',through='Ingredient_Measurement')
	yields = models.CharField(max_length=40, blank=True)
	instructions = models.TextField()
	durations = models.ManyToManyField('Duration', blank=True)
	photos = models.ManyToManyField('Photo', blank=True)
	summary = models.CharField(max_length=80, blank=True)
	published = models.DateField(blank=True)
	tags = models.ManyToManyField('Tag', blank=True)
	#custom fields
	#south is forcing a default. not sure why.
	url = models.SlugField(default='error')
	votes = models.IntegerField(default=1)
	users_voted = models.ManyToManyField(User, related_name='recipe_votes')
	submitor = models.ForeignKey(User, related_name='recipes_submitted')
	
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Recipe._meta.fields]
	
	def __unicode__(self):
		return self.name
	
	def meta(self):
		#default ordering
		ordering = ['-vote']
		
class Ingredient_Measurement(models.Model):
	ingredient = models.ForeignKey(Ingredient)
	recipe = models.ForeignKey(Recipe)
	value = models.CharField(max_length=20, blank=True)

class Duration(models.Model):
    """ The time it takes to prepare a recipe or a subset of a recipe """
    duration = models.CharField(max_length=40)
    def __unicode__(self):
        return self.duration

class Photo(models.Model):
    """ A photograph of delicious food """
    alt_text = models.CharField(max_length=40, default='')
    photo = models.ImageField(
            upload_to='recipe_images/%Y/%m/%d',
            blank=True)
    def __unicode__(self):
        return self.photo.name

class Tag(models.Model):
    """ A tag applied to a recipe for categorization and search """
    name = models.CharField(max_length=15)
    def __unicode__(self):
        return self.name
