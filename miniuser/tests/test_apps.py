# -*- coding: utf-8 -*-
"""miniuser's test base classes"""

# Python imports
from unittest import skip # noqa

# Django imports
from django.conf import settings
from django.test import override_settings

# app imports
from ..apps import set_app_default_setting
from .utils.testcases import MiniuserTestCase


class MiniUserConfigTest(MiniuserTestCase):
    """Tests targeting the app's AppConfig class"""

    def test_injection_working(self):
        """Can settings be injected in Django's setting module?

        Expected behaviour: setting is not present before it gets injected by
        set_app_default_setting()-method."""
        # setting is not present
        with self.assertRaises(AttributeError):
            self.assertEqual(settings.TEST_SETTING, 'foo')
        # inject the setting
        set_app_default_setting('TEST_SETTING', 'foo')
        # check if it was injected
        self.assertEqual(settings.TEST_SETTING, 'foo')

    @override_settings(TEST_SETTING='bar')
    def test_injections_respects_project_settings(self):
        """Injections respects already present settings from project's configuration

        Even after the call to set_app_default_setting()-method the value of
        TEST_SETTING is still 'bar'."""
        set_app_default_setting('TEST_SETTING', 'foo')
        self.assertEqual(settings.TEST_SETTING, 'bar')

    def test_injection_requires_capital_names(self):
        """In order to keep Django's conventions on settings, a full caps name is required

        'test_setting' will not be injected, because it does not follow the
        all caps convention."""
        set_app_default_setting('test_setting', 'foo')
        with self.assertRaises(AttributeError):
            self.assertEqual(settings.test_setting, 'foo')
