# -*- coding: utf-8 -*-
"""Application configuration"""

# Django imports
from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, Warning, register
from django.utils.translation import ugettext_lazy as _


E001 = Error(
    _("MINIUSER_DEFAULT_ACTIVE has to be True or False."),
    hint=_(
        "Please check your settings and ensure, that you put a boolean value "
        "to this setting."),
    id='miniuser.e001',
)

E002 = Error(
    _("MINIUSER_LOGIN_NAME has to be one of 'username', 'email' or 'both'."),
    hint=_(
        "Please check your settings and ensure, that MINIUSER_LOGIN NAME is one "
        "of 'username', 'email' or 'both'. Please note, that these values are "
        "given as strings."
    ),
    id='miniuser.e002',
)

E003 = Error(
    _("MINIUSER_REQUIRE_VALID_EMAIL has to be True or False."),
    hint=_(
        "Please check your settings and ensure, that you put a boolean value "
        "to this setting."),
    id='miniuser.e003',
)

E004 = Error(
    _("Values of MINIUSER_REQUIRE_VALID_EMAIL and MINIUSER_DEFAULT_ACTIVE do not match."),
    hint=_(
        "MINIUSER_REQUIRE_VALID_EMAIL = True implies MINIUSER_DEFAULT_ACTIVE = False. "
        "Check your settings!"
    ),
    id='miniuser.e004',
)

W001 = Warning(
    _("LOGIN_URL is *not* 'miniuser:login'."),
    hint=_(
        "If you want to use MiniUsers login-functions, add LOGIN_URL to your "
        "settings or modify its setting to 'miniuser:login'."
    ),
    id='miniuser.w001',
)


def check_correct_values(app_configs, **kwargs):
    """Checks, if all app specific settings have defined values"""

    errors = []

    if not isinstance(settings.MINIUSER_DEFAULT_ACTIVE, bool):
        errors.append(E001)
    if settings.MINIUSER_LOGIN_NAME not in ('username', 'email', 'both'):
        errors.append(E002)
    if not isinstance(settings.MINIUSER_REQUIRE_VALID_EMAIL, bool):
        errors.append(E003)

    return errors


def check_configuration_constraints(app_configs, **kwargs):
    """Checks, if the settings fullfill some (logical) constraints"""

    errors = []

    if settings.MINIUSER_REQUIRE_VALID_EMAIL and settings.MINIUSER_DEFAULT_ACTIVE:
        errors.append(E004)

    return errors


def check_configuration_recommendations(app_configs, **kwargs):

    errors = []

    if settings.LOGIN_URL != 'miniuser:login':
        errors.append(W001)

    return errors


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

        # checking, if all app specific settings got acceptable values
        register(check_correct_values)

        # check recommendations
        register(check_configuration_recommendations)

        # checking for some dependencies of the settings
        register(check_configuration_constraints)
