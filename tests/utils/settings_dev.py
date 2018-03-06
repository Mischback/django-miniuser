# -*- coding: utf-8 -*-
"""miniuser's test settings.

This file contains minimum settings to perform tests."""

# Python imports
import sys
from os.path import abspath, dirname, join, normpath

# path to the tests.util directory
TEST_ROOT = dirname(dirname(abspath(__file__)))

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
    'miniuser.apps.MiniUserConfig'
]

# apply our own user model
AUTH_USER_MODEL = 'miniuser.MiniUser'

# we need a test specific url configuration
ROOT_URLCONF = 'tests.utils.test_urls'

# respect app specific warning
LOGIN_URL = 'miniuser:login'

# this is a minimum test requirement
SECRET_KEY = 'only-for-testing'
