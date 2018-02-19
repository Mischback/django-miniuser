# -*- coding: utf-8 -*-
"""Application configuration"""

# Django imports
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# app imports
from .exceptions import MiniUserConfigurationException


def set_app_default_setting(name, default_value):
    """Injects app-specific settings into Django's settings-module. The function
    will take care of upper-case SETTING-names."""

    if name.isupper() and not hasattr(settings, name):
        setattr(settings, name, default_value)


class MiniUserConfig(AppConfig):
    """App specific configuration class"""

    name = 'miniuser'
    verbose_name = 'MiniUser'

    def ready(self):
        """Executed, when application loading is completed"""

        # setting some app specific (default) settings
        set_app_default_setting('MINIUSER_DEFAULT_ACTIVE', True)
        """Determines, if new users are active by default."""

        set_app_default_setting('MINIUSER_LOGIN_NAME', 'username')
        """Determines, if users can log in with
            a) their username (-> 'username'),
            b) their email-address (-> 'email') or
            c) both (-> 'both')."""

        set_app_default_setting('MINIUSER_REQUIRE_VALID_EMAIL', False)
        """Determines, if users must provide a valid email address. This also
        controls, if validation mails will be sent.

        Please note the connection with MINIUSER_LOGIN_NAME. If that setting is
        set to 'email', MINIUSER_REQUIRE_VALID_EMAIL has to be True."""

        # checking for some dependencies of the settings
        if (settings.MINIUSER_REQUIRE_VALID_EMAIL is True and settings.MINIUSER_DEFAULT_ACTIVE is True):
            raise MiniUserConfigurationException(
                _(
                    "Configuration mismatch! MINIUSER_REQUIRE_VALID_EMAIL = True implies"
                    "MINIUSER_DEFAULT_ACTIVE = False"
                )
            )
