# -*- coding: utf-8 -*-
"""Application configuration"""

# Django imports
from django.apps import AppConfig
from django.conf import settings


def set_app_default_setting(name, default_value):
    """Injects app-specific settings into Django's settings-module. The function
    will take care of upper-case SETTING-names."""

    if name.isupper() and not hasattr(settings, name):
        setattr(settings, name, default_value)


class MiniUserConfig(AppConfig):
    """App specific configuration class"""

    name = 'miniuser'
    verbose_name = 'MiniUser'

    def __init__(self, app_name, app_module):
        """Overriding the constructor to apply app specific settings into
        Django's setting module.

        This is necessary, because some of these settings are used in the
        definition of models.

        TODO: Find a way around that and move the injection into ready()"""

        # call the parent constructor
        super(MiniUserConfig, self).__init__(app_name, app_module)

        # setting some app specific (default) settings
        set_app_default_setting('MINIUSER_DEFAULT_ACTIVE', True)
        """Determines, if new users are active by default."""

        set_app_default_setting('MINIUSER_LOGIN_NAME', 'username')
        """Determines, if users can log in with
            a) their username,
            b) their email-address or
            c) both."""

    def ready(self):
        """Executed, when application loading is completed"""
        pass
