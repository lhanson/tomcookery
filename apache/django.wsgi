import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'tomcookery.settings'

# calculated paths for the project and its parent
SITE_ROOT = os.path.abspath(os.path.join(__file__, '../..'))
SITE_PARENT = os.path.abspath(os.path.join(SITE_ROOT, '../'))
#
sys.path.append(SITE_ROOT)
sys.path.append(SITE_PARENT)
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
