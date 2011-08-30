from django import forms
import re
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from tomcookery.app.models import *

difficultyChoice = (('-','Please Select'),('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Difficult', 'Difficult'))
courseChoice = (('-','Please Select'),('Appetizer', 'Appetizer'), ('Breakfast', 'Breakfast'), ('Dessert','Dessert'),('Entree','Entree'),('Lunch', 'Lunch'), ('Salad', 'Salad'), ('Soup', 'Soup'), ('Snack', 'Snack'))


class recipeNewSaveForm(forms.Form):
	name = forms.CharField(
	label=u'Name',
	widget=forms.TextInput(attrs={'size': 64, 'class':'required'})
	)
	ingredients = forms.CharField(
	required=True,
	widget=forms.HiddenInput(attrs={ 'class':'required'})
	) 
	
	summary = forms.CharField(
	widget=forms.Textarea(attrs={ 'class':'required'})
	)
	
	instructions = forms.CharField(
	label=u'Instructions',
	widget=forms.Textarea(attrs={ 'class':'required'})
	)
	
	photo=forms.ImageField(required=False)
	
	yields = forms.CharField(
	label=u'Number of servings?',
	required=False,
	widget=forms.TextInput(attrs={'size': 4})
	)
	
	durations = forms.CharField(
	required=False,
	widget=forms.TextInput(attrs={'size':4})
	)
	
	difficulty = forms.ChoiceField(
	required=True,
	widget=forms.Select(attrs={ 'class':'required'}),
	choices=difficultyChoice,
	)
	
	course = forms.ChoiceField(
	required=True,
	widget=forms.Select(attrs={ 'class':'required'}),
	choices=courseChoice,
	)
	
	tags = forms.CharField(
	label=u'Tags',
	widget=forms.TextInput(attrs={'size': 64, "placeholder":"e.g. thai, curry, easy",'class':'required'})
	)

class editProfile(ModelForm):
	class Meta:
		model=MyProfile
		exclude = ('recipePoints','commentPoints','votePoints','recipeLiked','chefRank','user')

class searchForm(forms.Form):
	query = forms.CharField(
		label=u'Enter a keyword to search for',
		widget = forms.TextInput(attrs={'size':32})
		)