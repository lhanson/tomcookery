from django.http import HttpResponse

def index(request):
    return HttpResponse("Main page")

def recipe(request, recipe_id):
    return HttpResponse("Displaying recipe " + recipe_id)

def recipes(request):
    return HttpResponse("Displaying recipes")
