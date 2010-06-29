from django.shortcuts import render_to_response
from tomcookery.app.models import Recipe

response_data = { 'app_name': 'Tomcookery' }

def index(request):
    return render_to_response('index.html', get_latest_recipes(response_data, 10))

def recipe(request, recipe_id):
    return render_to_response('recipe.html', get_recipe(response_data, recipe_id))

def recipes(request):
    return render_to_response('recipes.html', get_latest_recipes(response_data, 10))

def submit(request):
    return render_to_response('submit.html', response_data)

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
