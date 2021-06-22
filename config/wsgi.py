"""
WSGI config for easyborrow_depositor_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application


PROJECT_DIR_PATH = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
sys.path.append( PROJECT_DIR_PATH )

os.environ[u'DJANGO_SETTINGS_MODULE'] = 'config.settings'  # so django can access its settings



application = get_wsgi_application()
