from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from tomcookery.app.models import *
from tomcookery.app.forms import *
from .forms import ProfileForm
from django.conf import settings
import Image
import datetime
from django.core.files.base import ContentFile
import sys
sys.path.append("/Users/corygwin/djangoenv/lib/python2.6/site-packages/PIL-1.1.7-py2.6-macosx-10.3-fat.egg")

response_data = { 'app_name': 'Recipe Wars' }

def index(request):
	response_data.update({'moretoprecipes': Recipe.objects.all().order_by('published')[1:10] })
	response_data.update({'toprecipe': Recipe.objects.all().order_by('published')[0:1] })
	return render_to_response('index.html',
                              response_data,
                              context_instance = RequestContext(request))

def recipe(request, recipe_id):
    return render_to_response('recipe.html',
                              get_recipe(response_data, recipe_id),
                              context_instance = RequestContext(request))

def recipes(request):
    return render_to_response('recipes.html',
                              get_latest_recipes(response_data, 10),
                              context_instance = RequestContext(request))

@login_required
def profile(request):
    '''
    Displays page where user can update their profile.
    
    @param request: Django request object.
    @return: Rendered profile.html.
    '''
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print data

            #Update user with form data
            request.user.first_name = data['first_name']
            request.user.last_name = data['last_name']
            request.user.email = data['email']
            request.user.save()

            messages.success(request, 'Successfully updated profile!')
    else: 
        #Try to pre-populate the form with user data.
        form = ProfileForm(initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    response_data.update({'form': form, 'user': request.user})
    return render_to_response('profile.html',
                              response_data,
                              context_instance = RequestContext(request))

def _handleImageResize(image):
	path = settings.MEDIA_ROOT+"/"+str(image)
	print path
	im = Image.open(path)
	im.thumbnail((512,512), Image.ANTIALIAS)
	im.save(path)
                             
def _ingredientsProcess(ingString, recipe):
	for set in ingString.split(","):
		size, ing = set.split(";")
		ingObject, dummy = Ingredient.objects.get_or_create(
			name= ing
		)
		ingObject.hrecipe_set.add(recipe)
		ingObject.save()
	return recipe
			
@login_required
def submit(request):
    if request.method == 'POST':
        form = recipeNewSaveForm(request.POST,request.FILES)
        if form.is_valid():
			recipe = Recipe()
			recipe.name = form.cleaned_data['name']
			recipe.published = datetime.datetime.now()
			recipe.yields = form.cleaned_data['yields']
			recipe.instructions = form.cleaned_data['instructions']
			#recipe.photos = form.cleaned_data['photos']
			recipe.user = request.user
			#save the recipe because it needs a key before it can have many to many rels.
			recipe.save()
			#file_content = ContentFile(request.FILES['photo'].read())
			file = request.FILES['photo']
			photo = Photo.objects.create()
			photo.photo.save(file.name,file)
			photo.hrecipe_set.add(recipe)
			#now that we have the image lets resize it to a decent size
			_handleImageResize(photo.photo)
			for tagName in form.cleaned_data['tags'].split(","):
				if tagName != None:
					tag, dummy = Tag.objects.get_or_create(name=tagName.strip())
					tag.hrecipe_set.add(recipe)
					tag.save()
            
			durObject, dummy = Duration.objects.get_or_create(
				duration= form.cleaned_data['durations']
			)
			durObject.hrecipe_set.add(recipe)
			durObject.save()
			recipe = _ingredientsProcess(form.cleaned_data['ingredients'].rstrip('\n'), recipe)
            #ingredients = form.cleaned_data['ingredient'].split()
            #for ingredient in ingredients:
                #ingredientholder, dummy = recipe.objects.get_or_create(ingredients=ingredient)
                #Ingredient.tag_set.add(ingredientholder)
			recipe.save()
			return HttpResponseRedirect('/')
    else:
        form = recipeNewSaveForm()
    variables = RequestContext(request, {
        'form': form
    })
    
    return render_to_response('submit.html', response_data,
                              context_instance = variables)

def get_latest_recipes(dict, count):
    """ Add the latest 'count' recipes published to the given dictionary """
    dict.update({'recipes': Recipe.objects.all().order_by('published')[:count] })
    return dict

def get_recipe(dict, recipe_id):
    """ Adds the recipe corresponding to recipe_id to the given dictionary """
    print "Getting recipe " + recipe_id
    dict.update({'recipes': Recipe.objects.get(id=recipe_id)})
    print "Dictonary: " + repr(dict)
    return dict
