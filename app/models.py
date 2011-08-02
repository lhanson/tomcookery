from django.db import models
from django.contrib.auth.models import User
import os

class HRecipe(models.Model):
    """ Representation of an hrecipe-based recipe (see http://microformats.org/wiki/hrecipe) """
    name = models.CharField(max_length=40) # hrecipe field name is "fn"
    ingredients = models.ManyToManyField('Ingredient')
    yields = models.CharField(max_length=40, blank=True)
    instructions = models.TextField()
    durations = models.ManyToManyField('Duration', blank=True)
    photos = models.ManyToManyField('Photo', blank=True)
    summary = models.CharField(max_length=80, blank=True)
    authors = models.ManyToManyField('Author', blank=True)
    published = models.DateField(blank=True)
    nutrition = models.ManyToManyField('Nutrition', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    def __unicode__(self):
        return self.name

class Recipe(HRecipe):
    """ A recipe object """
    submitter = models.CharField(max_length=20)
    #replace submitter with a relationship to the user. below is what needs to happen, but south is not migrating.
    #not sure why but I suspect it has to do with the fixtures. Lyle can you look at this thanks :)
    #user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name + ", submitted by " + self.submitter

class Ingredient(models.Model):
    """ A single ingredient """
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        if self.value and self.type:
            return self.value + ' ' + self.type + ' ' + self.name
        else:
            return self.name

class Duration(models.Model):
    """ The time it takes to prepare a recipe or a subset of a recipe """
    duration = models.CharField(max_length=40)
    def __unicode__(self):
        return self.duration

class Photo(models.Model):
    """ A photograph of delicious food """
    alt_text = models.CharField(max_length=40, default='')
    #def get_image_path(instance, filename):
        #print "Getting image path for filename " + filename
        #path = os.path.join('photos', filename)
        #return path

    #photo = models.ImageField(
            #upload_to='recipe_images/%Y/%m/%d',
            #blank=True)
    def __unicode__(self):
        return self.photo.name

class Author(models.Model):
    """ The author of a recipe """
    name = models.CharField(max_length=40)
    # Note: hRecipe allows this element to be a full hCard, but for our purposes
    # a name string seems sufficient.
    def __unicode__(self):
        return self.name

class Nutrition(models.Model):
    """ Represents an element of nutritional information """
    value = models.CharField(max_length=40, blank=True)
    type = models.CharField(max_length=40, blank=True)

class Tag(models.Model):
    """ A tag applied to a recipe for categorization and search """
    name = models.CharField(max_length=15)
    def __unicode__(self):
        return self.name
