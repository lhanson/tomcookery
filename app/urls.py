from django.conf.urls.defaults import *
from django.conf import settings
from tomcookery.app import views
import os

urlpatterns = patterns('tomcookery.app.views',
    (r'^$', 'index'),
    (r'^recipes/$', 'recipes'),
    (r'^recipe/(?P<recipe_id>\d+)/$', 'recipe'),
    (r'^submit/$', 'submit'),
    #ajax calls
    (r'^ajax/tag/autocomplete/$', 'ajax_tag_autocompletion'),
)

urlpatterns += patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to',
            {'url': '/accounts/profile/', 'permanent': False},
            name='home'),
    # Account/Auth URLs not implemented by django_rpx_plus:
    url(r'^accounts/$', 'django.views.generic.simple.redirect_to', 
                        {'url': '/accounts/profile/', 'permanent': False},
                        name='auth_home'),
    url(r'^accounts/profile/$', 'app.views.profile', name='auth_profile'),
    #We will use django's built in logout view.
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
                      {'template_name': 'django_rpx_plus/logged_out.html'}, 
                      name='auth_logout'),
    # For django_rpx_plus
    (r'^accounts/', include('django_rpx_plus.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,'show_indexes': True}),
    
)

if settings.DEBUG:
    APP_ROOT = os.path.dirname(os.path.realpath(__file__))
    urlpatterns += patterns('',
        (r'^css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': APP_ROOT + '/CSS'}),
        (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.MEDIA_ROOT, 'photos')}),
    )
