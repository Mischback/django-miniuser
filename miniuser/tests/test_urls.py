# -*- coding: utf-8 -*-
"""miniuser's test base classes"""

# Python imports
from unittest import skip # noqa

# Django imports
from django.test import override_settings # noqa
from django.urls import reverse

# app imports
from .utils.testcases import MiniuserTestCase


class MiniUserUrlsTest(MiniuserTestCase):
    """Tests targeting the app's URL configuration"""

    def test_login_url(self):
        """Does reverse() return the right url?"""
        self.assertEqual('/login/', reverse('miniuser:login'))

    def test_logout_url(self):
        """Does reverse() return the right url?"""
        self.assertEqual('/logout/', reverse('miniuser:logout'))
