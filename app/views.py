from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from tomcookery.app.models import *
from tomcookery.app.forms import *
from django.conf import settings
import Image
import datetime
from django.core.files.base import ContentFile
import sys
from brabeion import badges
import brabeion.signals
from datetime import date, timedelta
import json
sys.path.append("/Users/corygwin/djangoenv/lib/python2.6/site-packages/PIL-1.1.7-py2.6-macosx-10.3-fat.egg")

response_data = { 
	'app_name': 'Recipe Wars', 
	'MEDIA_URL': settings.MEDIA_URL,
}

#views
##Landing pages
def index(request):
	if CookoffTheme.objects.all():
		response_data.update({'moretoprecipes': CookoffTheme.objects.currentThemeRecipesDate()[1:12]})
		response_data.update({'toprecipe':CookoffTheme.objects.currentThemeRecipesDate()[:1]})
	
	response_data.update(_rightColumnStandard())
	return render_to_response('index.html',
                              response_data,
                              context_instance = RequestContext(request))

def recipe(request, recipe_url):
	curRecipe = get_object_or_404(
		Recipe,
		url=recipe_url
	)
	
	ingredients = Ingredient_Measurement.objects.filter(recipe=curRecipe)
	response_data.update({'recipe':curRecipe,"ingredients":ingredients})
	return render_to_response('recipe.html',
                              response_data,
                              context_instance = RequestContext(request))

#right column
def _rightColumnStandard():
	week = date.today() - timedelta(weeks=1)
	if CookoffTheme.objects.all():
		return {'leadingRecipes': CookoffTheme.objects.currentThemeRecipesVotes()[:5]}
	else:
		return{}

##Tag based views
def tag_page(request, tag_name, model="Tag",urlParent=""):
	tag = get_object_or_404(model,id=tag_name)
	recipes=tag.recipe_set.all()
	variables = RequestContext(request,{
		'recipes': recipes,
		'title':"Recipes for %s" % tag.name,
		'tag_name':tag_name,
		'urlParent':urlParent
	})
	return render_to_response('tag_page.html',variables)

def tag_cloud_page(request, model="Tag",urlParent=""):
	MAX_WEIGHT = 5
	tags=model.objects.order_by("name")
	#calculate tag, min and max counts
	min_count = max_count = tags[0].recipe_set.count()
	for tag in tags:
		tag.count = tag.recipe_set.count()
		if tag.count < min_count:
			min_count = tag.count
		if max_count < tag.count:
			max_count = tag.count
	#calculate count range. Avoid dividing by 0
	range = float(max_count - min_count)
	if range == 0.0:
		range = 1.0
	#calculate tag weights
	for tag in tags:
		tag.weight = int(
			MAX_WEIGHT * (tag.count - min_count)/range
		)
	variables = RequestContext(request,{
		'tags':tags,
		'urlParent':urlParent
	})
	return render_to_response('tag_cloud_page.html',variables)
	
	

#voting
@login_required
def recipe_vote(request):
	'Recipe voting'
	if 'id' in request.GET:
		try:
			recipe_id = request.GET['id']
			recipe = Recipe.objects.get(id=recipe_id)
			user_voted = recipe.users_voted.filter(
				username = request.user.username
			)
			if not user_voted:
				recipe.votes += 1
				recipe.users_voted.add(request.user)
				recipe.save()
				submitor = recipe.submitor.get_profile()
				submitor.awardRecipeLiked(1)
				badges.possibly_award_badge("vote_submitted", user=request.user)
				profile = request.user.get_profile()
				profile.awardVote(1)
		except Recipe.DoesNotExist:
			raise Http404('Recipe Not Found')
	if 'HTTP_REFERER' in request.META:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	return HttpResponseRedirect('/')
			

#search
def search_page(request):
	form = searchForm()
	recipes = []
	show_results=False
	if 'query' in request.GET:
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = searchForm({'query':query})
			recipes=Recipe.objects.filter(
				name__icontains=query
				)[:10]
	variables = RequestContext(request,{
		'form':form,
		'recipes':recipes,
		'show_results':show_results,	
	})
	if request.GET.has_key('ajax'):
		return render_to_response('recipes_snippet.html',variables)
	else:
		return render_to_response('search.html',variables)


#recipe submission handlers
def _handleImageResize(image):
	path = settings.MEDIA_ROOT+"/"+str(image)
	im = Image.open(path)
	im.thumbnail((512,512), Image.ANTIALIAS)
	im.save(path)
                             
def _ingredientsProcess(ingString, recipe):
	jsonData = json.loads(ingString)
	print(jsonData)
	for set in jsonData:
		ingObject, dummy = Ingredient.objects.get_or_create(
			name= set['ingredient']
		)
		group = Ingredient_Measurement(ingredient=ingObject,recipe=recipe,value=set['measurement'])
		group.save()
	return recipe

def _get_badge(sender,**kwargs):
	return kwargs["badge_award"].slug
			
@login_required
def submit(request):
    if request.method == 'POST':
        form = recipeNewSaveForm(request.POST,request.FILES)
        if form.is_valid():
			from django.template.defaultfilters import slugify
			recipe = Recipe()
			recipe.name = form.cleaned_data['name']
			recipe.published = datetime.datetime.now()
			recipe.yields = form.cleaned_data['yields']
			recipe.summary = form.cleaned_data['summary']
			recipe.instructions = form.cleaned_data['instructions']
			#recipe.photos = form.cleaned_data['photos']
			recipe.submitor = request.user
			#save the recipe because it needs a key before it can have many to many rels.
			recipe.save()
			# create a url, we will make sure it is unique by adding the id number to the end.
			url = form.cleaned_data['name'] + "-" + str(recipe.id)
			recipe.url = slugify(url)
			recipe.users_voted.add(request.user)
			#file_content = ContentFile(request.FILES['photo'].read())
			try:
				if request.FILES['photo']:
					file = request.FILES['photo']
					photo = Photo.objects.create()
					photo.photo.save(file.name,file)
					photo.recipe_set.add(recipe)
					#now that we have the image lets resize it to a decent size
					#_handleImageResize(photo.photo)
			except:
				pass
			difficulty, dummy = Difficulty.objects.get_or_create(name=form.cleaned_data['difficulty'])
			difficulty.recipe_set.add(recipe)
			difficulty.save()
			course, dummy = Course.objects.get_or_create(name=form.cleaned_data['course'])
			course.recipe_set.add(recipe)
			course.save()
			for tagName in form.cleaned_data['tags'].split(","):
				if tagName != None:
					tag, dummy = Tag.objects.get_or_create(name=tagName.strip())
					tag.recipe_set.add(recipe)
					tag.save()
            
			durObject, dummy = Duration.objects.get_or_create(
				duration= form.cleaned_data['durations']
			)
			durObject.recipe_set.add(recipe)
			durObject.save()
			theme = CookoffTheme.objects.currentTheme()
			theme.recipes.add(recipe)
			theme.save()
			recipe = _ingredientsProcess(form.cleaned_data['ingredients'].rstrip('\n'), recipe)
			badges.possibly_award_badge("recipe_submitted", user=request.user)
			brabeion.signals.badge_awarded.connect(_get_badge)
			recipe.save()
			createUserProfile(request.user)
			profile = request.user.get_profile()
			profile.awardRecipe(1)
			redirectTo = "/recipes/recipe/%s" % recipe.url
			return HttpResponseRedirect(redirectTo)
    else:
        form = recipeNewSaveForm()
    variables = RequestContext(request, {
        'form': form
    })
    
    return render_to_response('submit.html', response_data,
                              context_instance = variables)




#ajax views
def ajax_tag_autocompletion(request):
	"tag parameter term and returns 10 tags that start with the query"
	if 'term' in request.GET:
		from django.utils import simplejson
		tags = Tag.objects.filter(
			name__istartswith = request.GET['term']
		)[:10]
		results = [ x.name for x in tags ]
		resp = simplejson.dumps(results)
		return HttpResponse(resp, mimetype='application/json')
	return HttpResponse()
	
def ajax_ingredient_autocompletion(request):
	"tag parameter term and returns 10 tags that start with the query"
	if 'term' in request.GET:
		from django.utils import simplejson
		tags = Ingredient.objects.filter(
			name__istartswith = request.GET['term']
		)[:10]
		results = [ x.name for x in tags ]
		resp = simplejson.dumps(results)
		return HttpResponse(resp, mimetype='application/json')
	return HttpResponse()