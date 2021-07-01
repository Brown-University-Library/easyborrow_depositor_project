"""
WSGI config for easyborrow_depositor_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

## original (works for runserver)
# import os, sys

# from django.core.wsgi import get_wsgi_application


# PROJECT_DIR_PATH = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
# sys.path.append( PROJECT_DIR_PATH )

# os.environ[u'DJANGO_SETTINGS_MODULE'] = 'config.settings'  # so django can access its settings

# application = get_wsgi_application()



import os, sys

import shellvars
from django.core.wsgi import get_wsgi_application


PROJECT_DIR_PATH = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
ENV_SETTINGS_FILE_PATH = os.environ['EZB_DEP__ENV_SETTINGS_PATH']  # set in `httpd/passenger.conf`, and `env/bin/activate`

sys.path.append( PROJECT_DIR_PATH )

os.environ[u'DJANGO_SETTINGS_MODULE'] = 'config.settings'  # so django can access its settings

## load up env vars
var_dct = shellvars.get_vars( ENV_SETTINGS_FILE_PATH )
for ( key, val ) in var_dct.items():
    os.environ[key.decode('utf-8')] = val.decode('utf-8')

application = get_wsgi_application()
