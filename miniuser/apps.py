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
        controls, if validation mails will be sent."""

        set_app_default_setting('LOGIN_URL', 'miniuser:login')
        """Set the app's login as the default login view.

        Please note, that Django already provides a value for this setting by
        default ('/accounts/login/'), so you have to override this value
        in your project's settings.
            LOGIN_URL = 'miniuser:login'

        Just in case somebody messed up his Django seriously, a sane default
        is provided here."""

        set_app_default_setting('LOGIN_REDIRECT_URL', '/')
        """Set a default redirect for successful logins.

        Please note, that Django already provides a value for this setting by
        default ('/accounts/profile/'), so you have to override this value
        in your project's settings.
            LOGIN_REDIRECT_URL = '/'
        You may specify other default redirects, obviously.

        Just in case somebody messed up his Django seriously, a sane default
        is provided here."""

        set_app_default_setting('LOGOUT_REDIRECT_URL', 'miniuser:login')
        """Set a default redirect for logouts. This will redirect the user to
        the login page.

        Please note, that Django already provides a value for this setting by
        default (None), so you have to override this value in your project's
        settings.
            LOGOUT_REDIRECT_URL = 'miniuser:login'
        You may specify other default redirects, obviously. Django's 'None'
        will render the logout template.

        Just in case somebody messed up his Django seriously, a sane default
        is provided here."""

        # checking for some dependencies of the settings
        if (settings.MINIUSER_REQUIRE_VALID_EMAIL is True and settings.MINIUSER_DEFAULT_ACTIVE is True):
            raise MiniUserConfigurationException(
                _(
                    "Configuration mismatch! MINIUSER_REQUIRE_VALID_EMAIL = True implies"
                    "MINIUSER_DEFAULT_ACTIVE = False"
                )
            )

        # in DEBUG-mode, notify the user possible problems with the settings
        if settings.DEBUG:
            # check LOGIN_URL
            if settings.LOGIN_URL != 'miniuser:login':
                # raise a Django warning!
                pass
