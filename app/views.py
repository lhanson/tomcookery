from django.shortcuts import render_to_response
from tomcookery.app.models import Recipe

response_data = { 'app_name': 'Tomcookery' }

def index(request):
    return render_to_response('index.html', getLatestRecipes(response_data, 10))

def recipe(request, recipe_id):
    return render_to_response('recipe.html', response_data)

def recipes(request):
    return render_to_response('recipes.html', getLatestRecipes(response_data, 10))

def submit(request):
    return render_to_response('submit.html', response_data)

def getLatestRecipes(dict, count):
    """ Add the latest 'count' recipes published to the given dictionary """
    dict.update({'recipes': Recipe.objects.all().order_by('published')[:count] })
    return dict
