#!/usr/bin/env python

# Python imports
import argparse
import os
import sys

# Django imports
from django import setup as django_setup
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import get_runner


class AppTestRunner(DiscoverRunner):
    """This subclass of Django's DiscoverRunner looks for tests in this directory

    Django's DiscoverRunner tries to find tests in the apps directory, specified
    by the name of the app. But the tests are seperated from the actual app
    code, so to build the suite, it has to discover tests here."""

    def build_suite(self, test_labels=None, extra_fields=None, **kwargs):
        """Override the build suite method to discover tests"""

        # TODO: Django's implementation does a lot of things. Are they necessary for this?

        # looking for tests in this directory
        suite = self.test_loader.discover('.')
        return suite


def run_tests():

    # this is necessary to actually connect with Django
    django_setup()

    # get the TestRunner (defaults to Django's implementation)
    # TODO: Make it possible to use another test runner
    # if not hasattr(settings, 'TEST_RUNNER'):
    #     settings.TEST_RUNNER = 'MyTestRunner'
    # TestRunner = get_runner(settings)
    test_runner = AppTestRunner()

    # running the suite
    failures = test_runner.run_tests('miniuser')

    return failures


if __name__ == '__main__':
    # set up the argument parser
    parser = argparse.ArgumentParser(description='Run the MiniUser test suite')
    parser.add_argument(
        '--settings',
        help="Python path to settings module, e.g. 'myproject.settings'. If "
             "this is not provided, 'tests.utils.settings_test' will be used."
    )

    # actually get the options
    options = parser.parse_args()

    # run tests according to the options
    if options.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'utils.settings_test')
        options.settings = os.environ['DJANGO_SETTINGS_MODULE']

    failures = run_tests()

    if failures:
        sys.exit(1)
