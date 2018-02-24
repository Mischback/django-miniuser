# -*- coding: utf-8 -*-
"""miniuser's test base classes"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.conf import settings
from django.test import override_settings

# app imports
from miniuser.apps import (
    E001, E002, E003, E004, W001, check_configuration_constraints,
    check_configuration_recommendations, check_correct_values,
    set_app_default_setting,
)

# app imports
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

    @override_settings(MINIUSER_DEFAULT_ACTIVE='foo')
    def test_check_e001(self):
        """MINIUSER_DEFAULT_ACTIVE must be a boolean value"""
        errors = check_correct_values(None)
        self.assertEqual(errors, [E001])

    @override_settings(MINIUSER_LOGIN_NAME='foo')
    def test_check_e002(self):
        """MINIUSER_LOGIN_NAME must be 'username', 'email' or 'both'"""
        errors = check_correct_values(None)
        self.assertEqual(errors, [E002])

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL='foo')
    def test_check_e003(self):
        """MINIUSER_REQUIRE_VALID_EMAIL must be a boolean value"""
        errors = check_correct_values(None)
        self.assertEqual(errors, [E003])

    @override_settings(MINIUSER_DEFAULT_ACTIVE=True)
    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=True)
    def test_check_e004(self):
        """MINIUSER_DEFAULT_ACTIVE and MINIUSER_REQUIRE_VALID_EMAIL must not be both True"""
        errors = check_configuration_constraints(None)
        self.assertEqual(errors, [E004])

    @override_settings(LOGIN_URL='/')
    def test_check_w001(self):
        """LOGIN_URL should be 'miniuser:login'"""
        errors = check_configuration_recommendations(None)
        self.assertEqual(errors, [W001])
