# -*- coding: utf-8 -*-
"""miniuser's app specific exceptions"""


class MiniUserException(Exception):
    """Base class for all app specific exceptions"""
    pass


class MiniUserConfigurationException(MiniUserException):
    """Raised, if there is a mismatch/inconsistency in the app specific settings."""
    pass
