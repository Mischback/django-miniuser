# -*- coding: utf-8 -*-
"""django-miniuser: Development/test settings.

This file contains minimum settings to run the development inside of
tox-environments and run the tests.

Please note, that some settings are explicitly set by the testrunner (see
runtests.py), i.e. migrations will be disabled by default during tests."""

# Python imports
import sys
from os.path import abspath, dirname, join, normpath

# path to the tests directory
TEST_ROOT = dirname(dirname(abspath(__file__)))

# path to the project directory
PROJECT_ROOT = dirname(TEST_ROOT)

# add PROJECT_ROOT to Python path
sys.path.append(normpath(PROJECT_ROOT))

# enable debugging (will be set to False by running tests)
DEBUG = True

# allow all hosts (will be set to [] by running tests)
ALLOWED_HOSTS = ['*']

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(TEST_ROOT, 'test.sqlite'),
    }
}

# minimum installed apps to make MiniUser work
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',   # introduced to make the admin usable inside tox
    'miniuser.apps.MiniUserConfig'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEST_ROOT,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# apply our own user model
AUTH_USER_MODEL = 'miniuser.MiniUser'

# we need a development/test specific url configuration
ROOT_URLCONF = 'tests.utils.urls_dev'

# respect app specific warning
LOGIN_URL = 'miniuser:login'

# provide a static URL for development
# introduced to make the admin usable inside tox
STATIC_URL = '/static/'

# this is a minimum test requirement
SECRET_KEY = 'only-for-testing'


# currently relevant for development!
# SEE #8802dd1!

MINIUSER_DEFAULT_ACTIVE = False
MINIUSER_ADMIN_SIGNUP_NOTIFICATION = {
    'django': ['mail'],
}

# just for development. Doesn't work for tests (locmem?)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
