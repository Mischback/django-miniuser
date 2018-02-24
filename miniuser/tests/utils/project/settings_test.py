# import the dev specific settings
# app imports
from .settings_dev import *  # noqa


# disable migrations during tests
# see https://simpleisbetterthancomplex.com/tips/2016/08/19/django-tip-12-disabling-migrations-to-speed-up-unit-tests.html # noqa
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        # return 'thesearenotthemigrationsyouarelookingfor'
        return None


MIGRATION_MODULES = DisableMigrations()
