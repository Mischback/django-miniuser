# -*- coding: utf-8 -*-
"""miniuser's app specific exceptions"""


class MiniUserException(Exception):
    """Base class for all app specific exceptions"""
    pass


class MiniUserConfigurationException(MiniUserException):
    """Raised, if there is a mismatch/inconsistency in the app specific settings."""
    pass


class MiniUserObjectActionException(MiniUserException):
    """Raised, if an exception must be raised during custom actions."""
    pass


class MiniUserActivateWithoutVerifiedEmailException(MiniUserObjectActionException):
    """Raised, if an account should be activated, that has no verified email
    address, while MINIUSER_REQUIRE_VALID_EMAIL = True"""
    pass


class MiniUserDeactivateOwnAccountException(MiniUserObjectActionException):
    """Raised, if a superuser tries to deactivate his own account"""
    pass
