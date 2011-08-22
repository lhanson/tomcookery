from django.db import models
from django.contrib.auth.models import User
import os
from brabeion import badges
from brabeion.base import Badge, BadgeAwarded
from django.shortcuts import get_object_or_404
import datetime
from sorl.thumbnail import ImageField

class Ingredient(models.Model):
    """ A single ingredient """
    name = models.CharField(max_length=20)
    def __unicode__(self):
    	return self.name

class Duration(models.Model):
    """ The time it takes to prepare a recipe or a subset of a recipe """
    duration = models.CharField(max_length=40)
    def __unicode__(self):
        return self.duration

class Difficulty(models.Model):
	"Different difficulty of recipe"
	name = models.CharField(max_length=15)
	
class Course(models.Model):
	"Different course of recipe"
	name = models.CharField(max_length=15)    



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
	difficulty = models.ForeignKey(Difficulty,blank=True,default="",null=True)
	course = models.ForeignKey(Course,blank=True,default="",null=True)
	
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Recipe._meta.fields]
	
	def __unicode__(self):
		return self.name
	
	def meta(self):
		#default ordering
		ordering = ['-vote']
	
	def get_absolute_url(self):
		return "/recipes/recipe/%s/" % self.url

class CookoffThemeManager(models.Manager):
	def currentTheme(self):
		query = self.filter(start_submit__lte=datetime.datetime.now(), end_vote__gte=datetime.datetime.now())
		if query:
			return query[0]
		else:
			return query


	def currentThemeRecipesDate(self):
		theme = self.currentTheme()
		if self.all():
			return theme.recipes.all().order_by('-published')
	
	def currentThemeRecipesVotes(self):
		theme = self.currentTheme()
		if self.all():
			return theme.recipes.all().order_by('-votes')

class CookoffTheme(models.Model):
	"Defines the model for the current theme of the recipe war"
	name = models.CharField(max_length=40)
	summary = models.TextField() 
	winning_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="winning_recipe")
	runner_up_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="second_recipe")
	third_place_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="third_recipe")
	recipes = models.ManyToManyField('Recipe', blank=True,null=True,related_name="all_recipes")
	start_submit = models.DateTimeField()
	end_submit = models.DateTimeField()
	start_vote = models.DateTimeField()
	end_vote = models.DateTimeField()
	
	objects = CookoffThemeManager()
	
	def submissionsOpen(self):
		"check to see if submission are open for the current war"
		return self.end_submit >= datetime.datetime.now() and self.start_submit <= datetime.datetime.now()
		
	def currentWarEntry(self,recipe):
		"add a recipe entry to a war"
		self.recipes.add(recipe)
		self.save()
		return recipe
	
	def voteOpen(self):
		"check if voting is open on a war"
		return self.end_vote >= datetime.datetime.now() and self.start_vote <= datetime.datetime.now()
	
	def currentThemeWinners(self):
		recipesbyrank = theme.recipes.all().order_by('-votes')[:2]
		self.winning_recipe = recipesbyrank[0]
		self.runner_up_recipe = recipesbyrank[1]
		self.third_place_recipe = recipesbyrank[2]
		self.save()
		return self
		
class Ingredient_Measurement(models.Model):
	ingredient = models.ForeignKey(Ingredient)
	recipe = models.ForeignKey(Recipe)
	value = models.CharField(max_length=20, blank=True)



class Photo(models.Model):
    """ A photograph of delicious food """
    alt_text = models.CharField(max_length=40, default='')
    photo = models.ImageField(
            upload_to='recipe_images/',
            blank=True)
    def __unicode__(self):
        return self.photo.name

class Tag(models.Model):
    """ A tag applied to a recipe for categorization and search """
    name = models.CharField(max_length=15)
    def __unicode__(self):
        return self.name

class ChefRank(models.Model):
	"Different ranks for users"
	name = models.CharField(max_length=15,default="Fry Cook")

def createUserProfile(user):
    """Create a UserProfile object each time a User is created ; and link it.
    """
    MyProfile.objects.get_or_create(user=user)

class MyProfile(models.Model):
	"Extends the user object for custom attr"
	user = models.OneToOneField(User)
	recipePoints = models.IntegerField(blank=True,default=0)
	commentPoints = models.IntegerField(blank=True,default=0)
	votePoints = models.IntegerField(blank=True,default=0)
	recipeLiked = models.IntegerField(blank=True,default=0) 
	website = models.URLField(blank=True,null=True,default="")
	websiteName = models.CharField(max_length=40,blank=True,null=True)
	chefRank = models.ForeignKey(ChefRank,blank=True,null=True)
	
	def awardVote(self,points):
		self.votePoints += points
		self.save()
	
	def awardRecipe(self,points):
		self.recipePoints += points
		self.save()
	
	def awardComment(self,points):
		self.commentPoints += points
		self.save()
	
	def awardRecipeLiked(self,points):
		self.recipeLiked += points
		self.save()
	
	User.profile = property(lambda u: MyProfile.objects.get_or_create(user=u)[0])
	
	def get_absolute_url(self):
		return ('profiles_profile_detail', (), { 'username': self.user.username })
	get_absolute_url = models.permalink(get_absolute_url)

#badges
class FirstRecipeBadge(Badge):
	slug = "Recipe Submitted"
	levels = [
	"Bronze"
	]
	events = [
	"recipe_submitted",
	]
	multiple = False
	user_message ="Recipe Submited Award"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		recipes = user.recipes_submitted.all()
		if len(recipes) == 1:
			return BadgeAwarded()

badges.register(FirstRecipeBadge)

class FirstRecipeVote(Badge):
	slug = "Recipe Vote"
	levels = [
	"Bronze"
	]
	events = [
	"vote_submitted",
	]
	multiple = False
	user_message ="Recipe Vote Award"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		votes = user.recipe_votes.all()
		if len(votes) == 1:
			return BadgeAwarded()

badges.register(FirstRecipeVote)
