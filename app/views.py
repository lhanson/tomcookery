from django.template import Context, loader
from tomcookery.app.models import Recipe
from django.http import HttpResponse

response_data = { 'app_name': 'Tomcookery' }

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(Context(response_data)))

def recipe(request, recipe_id):
    template = loader.get_template('recipe.html')
    recipe = Recipe(name='Hardcoded recipe name', submitter='Lyle')
    response_data.update({'recipe': recipe})
    return HttpResponse(template.render(Context(response_data)))

def recipes(request):
    template = loader.get_template('recipes.html')
    recipe1 = Recipe(name='Grilled cheese with beets', submitter='Lyle')
    recipe2 = Recipe(name='Limburger sandwich', submitter='Kelly')
    response_data.update({'recipes': [recipe1, recipe2]})
    return HttpResponse(template.render(Context(response_data)))

def submit(request):
    template = loader.get_template('submit.html')
    return HttpResponse(template.render(Context(response_data)))
