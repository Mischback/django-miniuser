# -*- coding: utf-8 -*-
"""Application configuration"""

# Django imports
from django.apps import AppConfig


class MiniUserConfig(AppConfig):
    """App specific configuration class"""

    name = 'miniuser'
    verbose_name = 'MiniUser'

    def ready(self):
        """Executed, when application loading is completed"""
        pass
