from django.conf.urls.defaults import *
from tomcookery.app.forms import editProfile
from tomcookery.app.models import createUserProfile

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #profile pages
    ('^profiles/edit', 'profiles.views.edit_profile', {'form_class': editProfile,}),
    ('^profiles/create', 'profiles.views.create_profile', {'form_class': editProfile,}),
    (r'^profiles/', include('profiles.urls')),
    url( r'^accounts/register/$',      'registration.views.register',
        { 'profile_callback': createUserProfile }, name = 'registration_register' ),
    (r'^accounts/', include('registration.urls')),
    (r'', include('app.urls')),
    
)
