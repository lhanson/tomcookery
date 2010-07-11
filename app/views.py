from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from tomcookery.app.models import Recipe, LoginForm, RPXForm
from tomcookery.app import settings
import urllib
import urllib2
import json

response_data = { 'app_name': 'Tomcookery' }

def index(request):
    response_data.update(get_user_login(response_data, request))
    return render_to_response('index.html', get_latest_recipes(response_data, 10))

def recipe(request, recipe_id):
    return render_to_response('recipe.html', get_recipe(response_data, recipe_id))

def recipes(request):
    return render_to_response('recipes.html', get_latest_recipes(response_data, 10))

def submit(request):
    return render_to_response('submit.html', response_data)

def rpx_callback(request):
    print "Got hit by the RPX callback!"
    if request.method == 'POST':
        form = RPXForm(request.POST)
        token = form.data['token']
        # Retrieve the user's data from RPX
        api_params = { 'apiKey': settings.JANDRAIN_API_KEY,
                       'token': token }
        http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info',
                                        urllib.urlencode(api_params))
        auth_info_json = http_response.read()
        auth_info = json.loads(auth_info_json)
        if auth_info['stat'] == 'ok':
            profile = auth_info['profile']
            print "Profile: "
            print profile
            # Unique ID used to sign in the user
            identifier = profile['identifier']
            displayName = profile.get('displayName')
            email = profile.get('email')
            profile_pic_url = profile.get('photo')
            # TODO: sign in user
            user = authenticate(username=displayName, password=identifier)
            if user is not None:
                if user.is_active:
                    print "Logging in..."
                    login(request, user)
                    # redirect to success page
                else:
                    print "Account is disabled" #TODO
            else:
                print "Registering new user..."
                user = User.objects.create_user(displayName, email, identifier)
                print "New user:"
                print user
                print "Authenticating..."
                print "New user:"
                print user
                user = authenticate(username=displayName, password=identifier)
                print "Authenticated:"
                print user
                print "Logging in..."
                login(request, user)
        else:
            print "An error occurred: " + auth_info['err']['msg']
    return HttpResponseRedirect('/')

def logout_view(request):
    """ Logs the current user out """
    logout(request)
    return HttpResponseRedirect('/')

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

def get_user_login(dict, request):
    dict.update({'logged_in': request.user.is_authenticated()})
    dict.update({'user': request.user})
    if not request.user.is_authenticated():
        dict.update({'form': LoginForm()})
    return dict
