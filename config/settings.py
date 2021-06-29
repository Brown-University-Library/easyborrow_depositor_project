"""
Django settings for easyborrow_depositor_project project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import json, os
from pathlib import Path


# =================================================
# project settings
# =================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# print( f'BASE_DIR, ``{BASE_DIR}``' )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['EZB_DEP__SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easyborrow_depositor_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

template_dirs = json.loads( os.environ['EZB_DEP__TEMPLATE_DIRS_JSON'] )
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': template_dirs,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.environ['EZB_DEP__CACHE_DIR_PATH'],
    }
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# db_dir = f'{BASE_DIR}/../db.sqlite3'
# print( f'db_dir, ``{db_dir}``' )
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': BASE_DIR / 'db.sqlite3',
#         'NAME': db_dir,
#     }
# }

db_json = json.loads( os.environ['EZB_DEP__DATABASES_JSON'] )
DATABASES = db_json


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'  # original setting is 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'

STATIC_URL = os.environ['EZB_DEP__STATIC_URL']
STATIC_ROOT = os.environ['EZB_DEP__STATIC_ROOT']  # needed for collectstatic command


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',  # note: configure server to use system's log-rotate to avoid permissions issues
            'filename': os.environ['EZB_DEP__LOG_PATH'],
            'formatter': 'standard',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'easyborrow_depositor_app': {
            'handlers': ['logfile'],
            'level': os.environ['EZB_DEP__LOG_LEVEL'],
            'propagate': False
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # 'django.db.backends': {  # re-enable to check sql-queries! <https://docs.djangoproject.com/en/1.11/topics/logging/#django-db-backends>
        #     'handlers': ['logfile'],
        #     'level': os.environ['EZB_DEP__LOG_LEVEL'],
        #     'propagate': False
        # },
    }
}


# =================================================
# app settings
# =================================================

BIB_OURL_API = os.environ['EZB_DEP__BIB_OURL_API_ROOT']

DEV_SHIB_DCT = json.loads( os.environ['EZB_DEP__DEV_SHIB_DCT_JSON'] )

# CACHE NOTE
# - Note that the `CACHES` setting, earlier in this file, contains the cache-location setting -- applicable to this and any other caching.
# - Cache is handled in seconds, so `PATTERN_LIB_CACHE_TIMEOUT` setting converts the envar hour-integer to seconds
# - Also, `LIB` instead of `HEADER` used for following setting because the header url _is_ to a header file specifically...
#   ...but it's likely that there will be at least another pattern-url; i.e. 'footer'.
PATTERNLIB_HEADER_CACHE_TIMEOUT = int( os.environ['EZB_DEP__PATTERNLIB_HEADER_CACHE_TIMEOUT_IN_HOURS'] ) * 60 * 60
PATTERNLIB_HEADER_URL = os.environ['EZB_DEP__PATTERNLIB_HEADER_URL']

FEEDBACK_FORM_URL = os.environ['EZB_DEP__FEEDBACK_FORM_URL_ROOT']
FEEDBACK_FORM_KEY = os.environ['EZB_DEP__FEEDBACK_FORM_KEY']
