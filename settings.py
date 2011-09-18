# Django settings for tomcookery project.
import os
import django,socket

if socket.gethostname() != 'Macintosh.local':
	#external settings file for production server
	from settings_production import *

else:
	#external settings for local test server
	from settings_local import *



ACCOUNT_ACTIVATION_DAYS = 7

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8p!+55am02)px6wm_l@f!+4#)nwy@5y1aa%jq4we5jt9i&4a9r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth', #for user template var
    #'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media', #for MEDIA_URL template var
    'django.core.context_processors.request', #includes request in RequestContext
    'django.contrib.messages.context_processors.messages',
    'tomcookery.app.custom_context.votingContext',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.csrf.CsrfResponseMiddleware',
	'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'tomcookery.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(SITE_ROOT, 'profiles'),
    os.path.join(SITE_ROOT, 'registration'),
)

# Auth backend config tuple does not appear in settings file by default. So we
# specify both the RpxBackend and the default ModelBackend:
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', #default django auth
)

#Settings for celery chron using ghettoq
CARROT_BACKEND = "django" 
CELERY_RESULT_BACKEND = "database" 
import djcelery
djcelery.setup_loader()

AUTH_PROFILE_MODULE="app.MyProfile"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.messages',
    'django.contrib.humanize',
    'tomcookery.registration',
    'tomcookery.app',
    'south',
    'tomcookery.brabeion',
    'tomcookery.profiles',
    'tomcookery.sorl.thumbnail',
    'tomcookery.djcelery',  
    'tomcookery.ghettoq',
    'tomcookery.djkombu',
    'tomcookery.pagination',
    'tomcookery.avatar',
)


REGISTER_URL = '/register/'

# Now load sensitive settings from a local file, if present
try:
    from local_settings import *
except Exception:
    pass

