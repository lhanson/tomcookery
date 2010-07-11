from django.conf.urls.defaults import *
from django.conf import settings
import os

urlpatterns = patterns('tomcookery.app.views',
    (r'^$', 'index'),
    (r'^recipes/$', 'recipes'),
    (r'^recipe/(?P<recipe_id>\d+)/$', 'recipe'),
    (r'^submit/$', 'submit'),
    (r'^profile/logout/$', 'logout_view'),
    (r'^rpx/$', 'rpx_callback'),
)

if settings.DEBUG:
    APP_ROOT = os.path.dirname(os.path.realpath(__file__))
    urlpatterns += patterns('',
        (r'^css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': APP_ROOT + '/CSS'}),
        (r'^photos/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(settings.MEDIA_ROOT, 'photos')}),
    )
