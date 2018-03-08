#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python imports
import argparse
import os
import sys

# Django imports
import django
from django.conf import settings
from django.test.utils import get_runner


def setup(enable_migrations, verbosity):
    """Prepares the test environment.

    Basically, this function is used to inject test-specific settings. It should
    be ensured, that these settings are only relevant to testing. A minimal
    configuration to actually run the app has to be specified using Django's
    setting-mechanism."""

    class DisableMigrations(object):
        """A generic class to disable all migrations during tests.

        See setup()-function on how this is applied."""

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            # return 'thesearenotthemigrationsyouarelookingfor'
            return None

    # don't test with debugging enabled
    settings.DEBUG = False
    settings.ALLOWED_HOSTS = []

    # disable migrations during tests
    if not enable_migrations:
        # see https://simpleisbetterthancomplex.com/tips/2016/08/19/django-tip-12-disabling-migrations-to-speed-up-unit-tests.html  # noqa
        settings.MIGRATION_MODULES = DisableMigrations()
        if verbosity >= 2:
            print('Testing without applied migrations.')
    else:
        if verbosity >= 2:
            print('Testing with applied migrations.')

    # actually build the Django configuration
    django.setup()


def app_tests(enable_migrations, tags, verbosity):
    """Gets the TestRunner and runs the tests"""

    # prepare the actual test environment
    setup(enable_migrations, verbosity)

    # reuse Django's DiscoverRunner
    if not hasattr(settings, 'TEST_RUNNER'):
        settings.TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    TestRunner = get_runner(settings)

    test_runner = TestRunner(
        verbosity=verbosity,
        tags=tags,
    )

    failures = test_runner.run_tests(['.'])

    return failures


if __name__ == '__main__':
    # set up the argument parser
    parser = argparse.ArgumentParser(description='Run the MiniUser test suite')
    parser.add_argument(
        '--enable-migrations', action='store_true', dest='enable_migrations',
        help="Enables the usage of migrations during tests."
    )
    parser.add_argument(
        '--settings',
        help="Python path to settings module, e.g. 'myproject.settings'. If "
             "this is not provided, 'tests.utils.settings_dev' will be used."
    )
    parser.add_argument(
        '-t', '--tag', dest='tags', action='append',
        help="Run only tests with the specified tags. Can be used multiple times."
    )
    parser.add_argument(
        '-v', '--verbosity', default=1, type=int, choices=[0, 1, 2, 3],
        help="Verbosity level; 0=minimal, 3=maximal; default=1"
    )

    # actually get the options
    options = parser.parse_args()

    # run tests according to the options
    if options.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'utils.settings_dev')
        options.settings = os.environ['DJANGO_SETTINGS_MODULE']

    failures = app_tests(
        options.enable_migrations,
        options.tags,
        options.verbosity,
    )

    if failures:
        sys.exit(1)
