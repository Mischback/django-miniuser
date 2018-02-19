# -*- coding: utf-8 -*-
"""miniuser's test settings.

This file contains minimum settings to perform tests."""

# Python imports
from os.path import abspath, dirname, join


# path to the test.util directory
TEST_ROOT = dirname(dirname(abspath(__file__)))

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
ROOT_URLCONF = 'miniuser.tests.utils.project.urls'

# respect app specific warning
LOGIN_URL = 'miniuser:login'

# this is a minimum test requirement
SECRET_KEY = 'only-for-testing'
