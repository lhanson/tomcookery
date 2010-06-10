from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'tomcookery.app.views.index'),
    (r'^recipes/$', 'tomcookery.app.views.recipes'),
    (r'^recipe/(?P<recipe_id>\d+)/$', 'tomcookery.app.views.recipe'),
    (r'^submit/$', 'tomcookery.app.views.submit'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
