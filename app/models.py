from django.db import models
from django.contrib.auth.models import User
import os
from brabeion import badges
from brabeion.base import Badge, BadgeAwarded
from django.shortcuts import get_object_or_404
import datetime
from sorl.thumbnail import ImageField
from django.db.models import F
from django.contrib import messages

class Ingredient(models.Model):
    """ A single ingredient """
    name = models.CharField(max_length=255)
    def __unicode__(self):
    	return self.name

class Duration(models.Model):
    """ The time it takes to prepare a recipe or a subset of a recipe """
    duration = models.CharField(max_length=255)
    def __unicode__(self):
        return self.duration

class Difficulty(models.Model):
	"Different difficulty of recipe"
	name = models.CharField(max_length=150)
	
class Course(models.Model):
	"Different course of recipe"
	name = models.CharField(max_length=150)    



class Recipe(models.Model):
	""" Representation of an hrecipe-based recipe (see http://microformats.org/wiki/hrecipe) """
	name = models.TextField() # hrecipe field name is "fn"
	ingredients = models.ManyToManyField('Ingredient',through='Ingredient_Measurement')
	yields = models.CharField(max_length=255, blank=True)
	instructions = models.TextField()
	durations = models.ManyToManyField('Duration', blank=True)
	photos = models.ManyToManyField('Photo', blank=True)
	summary = models.TextField()
	published = models.DateField(blank=True)
	tags = models.ManyToManyField('Tag', blank=True)
	#custom fields
	url = models.SlugField(default='error')
	votes = models.IntegerField(default=1)
	votes_ing = models.IntegerField(default=1)
	votes_theme = models.IntegerField(default=1)
	votes_custom = models.IntegerField(default=1)
	#users_voted = models.ManyToManyField(User, related_name='recipe_votes')
	submitor = models.ForeignKey(User, related_name='recipes_submitted')
	difficulty = models.ForeignKey(Difficulty,blank=True,null=True)
	course = models.ForeignKey(Course,blank=True,null=True)
	views = models.IntegerField(default=1)
	
	def recipeTheme(self):
		return CookoffTheme.objects.filter(recipes=self)[0]
	
	def votingOpen(self):
		"Return true of false voting for this recipe is open"
		return CookoffTheme.objects.filter(recipes=self)[0].voteOpen()
	
	def get_fields(self):
		"returns all field for this item"
		return [(field.name, field.value_to_string(self)) for field in Recipe._meta.fields]
	
	def __unicode__(self):
		return self.name
	
	def meta(self):
		#default ordering
		ordering = ['-vote']
	
	def get_absolute_url(self):
		return "/recipes/recipe/%s/" % self.url
	
	def recipe_view(self):
		"Increment view counter"
		self.views = F('views') + 1
		self.save()
	
	def overallVote(self,user):
		"Increment overall counter"
		self.votes = F('votes') + 1
		self.save()
		u = user.get_profile()
		u.users_voted_overall.add(self.recipeTheme())
		u.save()
		
	def ingVote(self,user):
		"Increment overall counter"
		self.votes_ing = F('votes_ing') + 1
		self.save()
		u = user.get_profile()
		u.users_voted_ing.add(self.recipeTheme())
		u.save()
		
	def themeVote(self,user):
		"Increment overall counter"
		self.votes_theme = F('votes_theme') + 1
		self.save()
		u = user.get_profile()
		u.users_voted_theme.add(self.recipeTheme())
		u.save()
		
	def customVote(self,user):
		"Increment overall counter"
		self.votes_custom = F('votes_custom') + 1
		self.save()
		
	def get_share_url(self):
		"URL for share tools"
		from django.contrib.sites.models import Site
		return 'http://www.recipe-wars.com/%s' %  self.get_absolute_url()
							
	def get_share_title(self):
		"title for share tools"
		return self.name
	
	def get_share_description(self):
		"descrioption for share tools"
		return '%s...' % self.summary[:512]



class CookoffThemeManager(models.Manager):
	def currentTheme(self):
		"Returns the currently active theme object only 1 allowed at a time"
		query = self.filter(start_submit__lte=datetime.datetime.now(), end_vote__gte=datetime.datetime.now())
		#print(query)
		if query:
			return query[0]
		else:
			return query
			
	def recentlyClosedTheme(self):
		"Returns the currently active theme object only 1 allowed at a time"
		query = self.filter(end_vote__lt=datetime.datetime.now()).order_by('-end_vote')
		#print(query)
		if query:
			return query[0]
		else:
			return query
			
	def currentThemeRecipesDate(self):
		"returns all recipes for the current theme ordered by date"
		theme = self.currentTheme()
		try:
			return theme.recipes.all().order_by('-published')
		except:
			return {}
	def currentThemeRecipesVotes(self, order="-votes"):
		"returns all recipes for the current theme ordered by defined order"
		theme = self.currentTheme()
		try:
			return theme.recipes.all().order_by(order)
		except:
			return {}
	
	
	def closeTheme(self):
		"Checks if a theme ended today, if so get and set winners"
		themes = CookoffTheme.objects.all().order_by('-end_vote')[0:1]
		for theme in themes:
			if theme.votingEndedToday():
				theme.currentThemeWinners()
				
			
class CookoffTheme(models.Model):
	"Defines the model for the current theme of the recipe war"
	slug = models.SlugField(max_length=255,blank=True,null=True)
	#theme descritptions
	name = models.CharField(max_length=255)
	summary = models.TextField()
	theme = models.CharField(max_length=255,blank=True,null=True)
	ingredient = models.ForeignKey('Ingredient',blank=True,null=True)
	photos = models.ManyToManyField('Photo', blank=True)
	#overall winners
	winning_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="winning_recipe")
	runner_up_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="second_recipe")
	third_place_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="third_recipe")
	#theme use
	winning_theme_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="winning_theme_recipe")
	runner_up_theme_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="second_theme_recipe")
	third_place_theme_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="third_theme_recipe")
	#ing use
	winning_ing_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="winning_ing_recipe")
	runner_up_ing_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="second_ing_recipe")
	third_place_ing_recipe = models.ForeignKey('Recipe',blank=True,null=True,related_name="third_ing_recipe")
	#all recipes
	recipes = models.ManyToManyField('Recipe', blank=True,null=True,related_name="all_recipes")
	#contest runs dates
	start_submit = models.DateTimeField()
	end_submit = models.DateTimeField()
	start_vote = models.DateTimeField()
	end_vote = models.DateTimeField()
	#custom_criteria = models.CharField(max_length=140)
	
	objects = CookoffThemeManager()
	
	def votingEndedToday(self):
		"Check if the theme voting ended today"
		return self.end_vote.date() == datetime.date.today()
	
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
		"Get the top three voted recipes and set the winners"
		recipesbyrank = self.recipes.all().order_by('-votes')[:3]
		self.winning_recipe = recipesbyrank[0]
		#we will award a badge, since we know what badge to award we will not check in the badge class
		#instead we will pass a keyword of what and a number of the place
		badges.possibly_award_badge("end_theme", user=recipesbyrank[0].submitor,theme=self,award="overall1")
		self.runner_up_recipe = recipesbyrank[1]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[1].submitor,theme=self,award="overall2")
		self.third_place_recipe = recipesbyrank[2]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[2].submitor,theme=self,award="overall3")
		recipesbyrank = self.recipes.all().order_by('-votes_theme')[:3]
		self.winning_theme_recipe = recipesbyrank[0]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[0].submitor,theme=self,award="themeuse1")
		self.runner_up_theme_recipe = recipesbyrank[1]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[1].submitor,theme=self,award="themeuse2")
		self.third_place_theme_recipe = recipesbyrank[2]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[2].submitor,theme=self,award="themeuse3")
		recipesbyrank = self.recipes.all().order_by('-votes_ing')[:3]
		self.winning_ing_recipe = recipesbyrank[0]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[0].submitor,theme=self,award="ing1")
		self.runner_up_ing_recipe = recipesbyrank[1]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[1].submitor,theme=self,award="ing2")
		self.third_place_ing_recipe = recipesbyrank[2]
		badges.possibly_award_badge("end_theme", user=recipesbyrank[2].submitor,theme=self,award="ing3")
		self.save()
		return self
	
	def get_absolute_url(self):
		return "/themes/theme/%s/" % self.id
		
class Ingredient_Measurement(models.Model):
	ingredient = models.ForeignKey(Ingredient)
	recipe = models.ForeignKey(Recipe)
	value = models.CharField(max_length=255, blank=True)



class Photo(models.Model):
    """ A photograph of delicious food """
    alt_text = models.CharField(max_length=255, default='')
    photo = models.ImageField(
            upload_to='recipe_images/',
            blank=True)
    def __unicode__(self):
        return self.alt_text

class Tag(models.Model):
    """ A tag applied to a recipe for categorization and search """
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class ChefRank(models.Model):
	"Different ranks for users"
	name = models.CharField(max_length=255,default="Fry Cook")

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
	website = models.URLField(blank=True,null=True)
	websiteName = models.CharField(max_length=255,blank=True,null=True)
	chefRank = models.ForeignKey(ChefRank,blank=True,null=True)
	twitterHandle=models.CharField(max_length=255,blank=True,null=True)
	
	#keep track of users voting actions on themes
	users_voted_ing = models.ManyToManyField(CookoffTheme, related_name='recipe_votes_ing',blank=True,null=True)
	users_voted_theme = models.ManyToManyField(CookoffTheme, related_name='recipe_votes_theme',blank=True,null=True)
	users_voted_overall = models.ManyToManyField(CookoffTheme, related_name='recipe_votes_overall',blank=True,null=True)
	#users_voted_custom = models.ManyToManyField(User, related_name='recipe_votes_custom')
	
	def userVotedThemeIng(self,theme):
		"Checks if the user has voted for the best ingredient use for given theme"
		if len(self.users_voted_ing.filter(id=theme.id)) > 0:
			return False
		return True
		
	def userVotedThemeOverall(self,theme):
		"Checks if the user has voted for the best overall recipe for given theme"
		if len(self.users_voted_overall.filter(id=theme.id)) > 0:
			return False
		return True
		
	def userVotedThemeTheme(self,theme):
		"Checks if the user has voted for the best theme use for given theme"
		if len(self.users_voted_theme.filter(id=theme.id)) > 0:
			return False
		return True
	
	def voteRecord(self,theme,action,request):
		if action == "overall":
			self.users_voted_overall.add(theme)
		elif action == "ing":
			self.users_voted_ing.add(theme)
		elif action == "theme":
			self.users_voted_theme.add(theme)
		#elif action == "custom":
			#self.users_voted_theme.add(theme)
		self.awardVote("1",request)
		
	def awardVote(self,points,request):
		self.votePoints += points
		self.save()
		self.chefStatus(request)
		
	def awardRecipe(self,points,request):
		self.recipePoints += points
		self.save()
		self.chefStatus(request)
		
	def awardComment(self,points,request):
		self.commentPoints += points
		self.save()
		self.chefStatus(request)
		
	def awardRecipeLiked(self,points,request):
		self.recipeLiked += points
		self.save()
		self.chefStatus(request)
		
	def chefStatus(self,request):
		chefPoints = self.recipePoints + self.recipeLiked
		criticPoints = self.commentPoints + self.votePoints
		totalPoints = chefPoints + criticPoints
		if totalPoints < 70:
			if totalPoints < 2:
				rank = "Patron"
			elif totalPoints < 10:
				rank = "Frequent Visitor"
			elif totalPoints < 22:
				rank = "Aspiring Cook"
			elif totalPoints < 40:
				rank = "Recipe Fan"
			else:
				rank = "Foodie"	
		elif chefPoints > criticPoints:
			if chefPoints < 30:
				rank = "Home Cook"
			elif chefPoints < 40:
				rank = "Chef in Training"
			elif chefPoints < 50:
				rank = "Fry Cook"
			elif chefPoints < 60:
				rank = "Line Cook"
			else:
				rank = "Chef"
		elif criticPoints > chefPoints:
			if criticPoints < 30:
				rank = "Food Snob"
			elif chefPoints < 50:
				rank = "Recipe Critic"
			elif chefPoints < 60:
				rank = "Food Reviewer"
			elif chefPoints < 80:
				rank = "Restaraunt Reviewer"
			else:
				rank = "Food critic"
		else:
			rank = "Foodie"
		if self.chefRank == None or rank != self.chefRank.name:
			rankObj, dummy = ChefRank.objects.get_or_create(name=rank)
			self.chefRank = rankObj
			messagetosend = "Congratulations you have acheived the status of %s" % self.chefRank.name
			messages.add_message(request, messages.INFO,messagetosend)
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
		if user.get_profile().votePoints == 1:
			return BadgeAwarded()

badges.register(FirstRecipeVote)


class BestRecipeOverall(Badge):
	slug = "Best Recipe Overall"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="Congratulations, your recipe was voted the best recipe of the theme!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "overall1":
			return BadgeAwarded()

badges.register(BestRecipeOverall)

class SecondBestRecipeOverall(Badge):
	slug = "Second Overall"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="Your stellar chef skills almost got you the win, your recipe was voted the second best recipe of the theme!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "overall2":
			return BadgeAwarded()
			
badges.register(SecondBestRecipeOverall)

class ThirdBestRecipeOverall(Badge):
	slug = "Third Overall"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="Third place overall! Next time use more bacon and you will win the theme for sure!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "overall3":
			return BadgeAwarded()

badges.register(ThirdBestRecipeOverall)

class BestThemeUseOverall(Badge):
	slug = "Best Use of Theme"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="Your cleverness and research won over some peoples hearts, your recipe was voted the best use of theme!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "themeuse1":
			return BadgeAwarded()

badges.register(BestThemeUseOverall)

class SecondBestThemeUse(Badge):
	slug = "Second best theme use"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="If only you could cook as well as you can research, you won second best use of theme!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "themeuse2":
			return BadgeAwarded()

badges.register(SecondBestThemeUse)

class ThirdBestThemeUse(Badge):
	slug = "Third best theme use"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="Your almost as brilliant as those two people with better theme uses, that still makes you gifted and talented in our book! You got third best use of theme!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "themeuse3":
			return BadgeAwarded()

badges.register(ThirdBestThemeUse)

class BestIngredientUseOverall(Badge):
	slug = "Best Use of Ingredient"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="Your commanding knowledge of ingredients has shown through to your comrades, congrats you wielded you ingredients with great poise and won best use of ingredient!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "ing1":
			return BadgeAwarded()

badges.register(BestIngredientUseOverall)

class SecondBestIngredientUse(Badge):
	slug = "Second best ingredient use"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="If this one ingriedient where the key to all cooking you would be amazing, your recipe was voted second best use of ingredient!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "ing2":
			return BadgeAwarded()

badges.register(SecondBestIngredientUse)

class ThirdBestIngredientUse(Badge):
	slug = "Third best ingredient use"
	levels = [
	"Bronze"
	]
	events = [
	"end_theme",
	]
	multiple = True
	user_message ="Ingredients, there are so many of them but you seem to have a pretty good handle on this one, your recipe was voted third best use of ingredient!"
	def award(self, **state):
		user=get_object_or_404(User,username=state["user"].username)
		if state["award"] == "ing3":
			return BadgeAwarded()

badges.register(ThirdBestThemeUse)

#signal listeners
from django.contrib.comments.signals import comment_will_be_posted

def commentCallback(sender, comment, request, **kwargs):
	"The signal listener call this then it awards a comment point to the user"
	request.user.get_profile().awardComment(1,request)

comment_will_be_posted.connect(commentCallback)

