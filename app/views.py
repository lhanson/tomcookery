from django.template import Context, loader
from tomcookery.app.models import Recipe
from django.http import HttpResponse

def index(request):
    return HttpResponse("Main page")

def recipe(request, recipe_id):
    template = loader.get_template('recipe.html')
    context = Context({
        'name': 'Hardcoded recipe name',
    })
    return HttpResponse(template.render(context))

def recipes(request):
    return HttpResponse("Displaying recipes")

def submit(request):
    template = loader.get_template('submit.html')
    context = Context({})
    return HttpResponse(template.render(context))
