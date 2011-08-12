from django.conf.urls.defaults import *
from django.conf import settings
from tomcookery.app.views import *
from tomcookery.app.models import *
from django.views.generic.simple import direct_to_template
import os

urlpatterns = patterns('tomcookery.app.views',
	#landing pages
    (r'^$', 'index'),
    (r'^tag/([^\s]+)/$',tag_page,{"model":Tag}),
    (r'^tag/$',tag_cloud_page,{"model":Tag,"urlParent":"tag"}),
    (r'^ingredients/([^\s]+)/$',tag_page,{"model":Ingredient}),
    (r'^ingredients/$',tag_cloud_page,{"model":Ingredient,"urlParent":"ingredients"}),
    #search
    (r'^search/$',search_page),
    #recipe voting
    (r'^vote/','recipe_vote'),
    (r'^recipes/recipe/(?P<recipe_url>[a-zA-Z0-9_.-]+)/$', 'recipe'),
    (r'^submit/$', 'submit'),
    #ajax calls
    (r'^ajax/tag/autocomplete/$', 'ajax_tag_autocompletion'),
    (r'^ajax/ingredient/autocomplete/$', 'ajax_ingredient_autocompletion'),
    #registration
    (r'^register/$', "register_page"),
    (r'^register/success/$',direct_to_template,{'template':'registration/register_success.html'}),
)

urlpatterns += patterns('',
	#media path
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,'show_indexes': True}),
    #login
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #logout
    (r'^logout/$', logout_page),
    #comments
    (r'^comments/',include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    APP_ROOT = os.path.dirname(os.path.realpath(__file__))
    urlpatterns += patterns('',
        (r'^css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': APP_ROOT + '/CSS'}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': APP_ROOT + '/js'}),
        (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.MEDIA_ROOT, 'photos')}),
    )
