"""
Django settings for siaiepi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from django.utils.translation import ugettext_lazy as _

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l7&!d+3p38#!f3udikw8ekxh(e#lhq#dzow2rc&cifi(-#lpwu'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-fi
#########
# PATHS #
#########
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
# Application definition

INSTALLED_APPS = (
    'modern_business',
    'suit',
    'solo',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'highcharts',
    'mptt',
    'compressor',
    'easy_thumbnails',
    'django_datatable_view_extension',
    'poll',
    'config',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'siaiepi.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'siaiepi.urls'

WSGI_APPLICATION = 'siaiepi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

# DATETIME_INPUT_FORMATS = (
#     '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
# )
#
# DATE_INPUT_FORMATS = (
#     '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
# )
#
# DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Redirect when login is correct.
LOGIN_REDIRECT_URL = "/poll/questionnaire"
# Redirect when login is not correct.
LOGIN_URL = '/'

# ALLOWED_HOSTS = ['*']
#
DEBUG = True

########################
# SETTINGS DJANGO-SUIT #
########################
SUIT_CONFIG = {
    'ADMIN_NAME': _('SI-IMCI'),
    # 'MENU': (
    #     # Keep original label and models
    #     'sites',
    #     # Rename app and set icon
    #     {'app': 'auth', 'label': 'Authorization', 'icon':'icon-lock'},
    #     # Reorder app models
    #     {'app': 'auth', 'models': ('user', 'group')},
    #     # Custom app, with models
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     # Cross-linked models with custom name; Hide default icon
    #     {'label': 'Custom', 'icon':None, 'models': (
    #         'auth.group',
    #         {'model': 'auth.user', 'label': 'Staff'}
    #     )},
    #     # Custom app, no models (child links)
    #     {'label': 'Users', 'url': 'auth.user', 'icon':'icon-user'},
    #     # Separator
    #     '-',
    #     # Custom app and model with permissions
    #     {'label': 'Secure', 'permissions': 'auth.add_user', 'models': [
    #         {'label': 'custom-child', 'permissions': ('auth.add_user', 'auth.add_group')}
    #     ]},
    # )
}

# Local settings
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'warning',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

ALLOWED_EXTERNAL_ACCESS_VIEW = [
    'login',
]

try:
    execfile(os.path.join(BASE_DIR, 'siaiepi', 'local_settings.py'))
except IOError:
    pass
