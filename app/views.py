from django.shortcuts import render_to_response
from tomcookery.app.models import Recipe
from tomcookery.app.models import HRecipe
from django.template import RequestContext
from tomcookery.app.forms import *

response_data = { 'app_name': 'Tomcookery' }

def index(request):
    return render_to_response('index.html', get_latest_recipes(response_data, 10))

def recipe(request, recipe_id):
    return render_to_response('recipe.html', get_recipe(response_data, recipe_id))

def recipes(request):
    return render_to_response('recipes.html', get_latest_recipes(response_data, 10))

def get_latest_recipes(dict, count):
    """ Add the latest 'count' recipes published to the given dictionary """
    dict.update({'recipes': Recipe.objects.all().order_by('published')[:count] })
    return dict

def get_recipe(dict, recipe_id):
    """ Adds the recipe corresponding to recipe_id to the given dictionary """
    print "Getting recipe " + recipe_id
    dict.update({'recipe': Recipe.objects.get(id=recipe_id)})
    print "Dictonary: " + repr(dict)
    return dict

def recipe_save_page(request):
	if request.method == 'POST':
		form = recipeNewSaveForm(request.POST)
		if form.is_valid():
			recipe.name = form.cleaned_data['name']
			recipe.yeilds = form.cleaned_data['yields']
			recipe.instructions = form.cleaned_data['instructions']
			recipe.durations = form.cleaned_data['durations']
			recipe.photos = form.cleaned_data['photos']
			recipe.name = form.cleaned_data['name']
			recipe.author = request.user
			tagNames = form.cleaned_data['tags'].split()
			for tagName in tagNames:
				tag, dummy = recipe.objects.get_or_create(name=tag_name)
				Tag.tag_set.add(tag)
			ingredients = form.cleaned_data['ingredient'].split()
			for ingredient in ingredients:
				ingredientholder, dummy = recipe.objects.get_or_create(ingredients=ingredient)
				Ingredient.tag_set.add(ingredientholder)
			recipe.save()
			return HTTPResponseRedirect ('/')
	else:
		form = recipeNewSaveForm()
	variables = RequestContext(request, {
    	'form': form
  	})
	return render_to_response('submit.html', variables)