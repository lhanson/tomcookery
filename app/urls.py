from django.conf.urls.defaults import *

urlpatterns = patterns('tomcookery.app.views',
    (r'^$', 'index'),
    (r'^recipes/$', 'recipes'),
    (r'^recipe/(?P<recipe_id>\d+)/$', 'recipe'),
    (r'^submit/$', 'submit'),
)
