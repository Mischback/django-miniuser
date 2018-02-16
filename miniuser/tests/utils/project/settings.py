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
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'miniuser.apps.MiniUserConfig'
]

AUTH_USER_MODEL = 'miniuser.MiniUser'

# this is a minimum test requirement
SECRET_KEY = 'only-for-testing'

# disable migrations during tests
# see https://simpleisbetterthancomplex.com/tips/2016/08/19/django-tip-12-disabling-migrations-to-speed-up-unit-tests.html
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        # return 'thesearenotthemigrationsyouarelookingfor'
        return None

MIGRATION_MODULES = DisableMigrations()
