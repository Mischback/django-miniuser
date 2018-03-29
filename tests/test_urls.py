# -*- coding: utf-8 -*-
"""django-miniuser: Tests for the app's url configuration

These tests target the code in miniuser/urls.py."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag  # noqa
from django.urls import reverse

# app imports
from .utils.testcases import MiniuserTestCase


@tag('urls')
class MiniUserUrlsTest(MiniuserTestCase):
    """Tests targeting the app's URL configuration"""

    def test_login_url(self):
        """Does reverse() return the right url?"""
        self.assertEqual('/login/', reverse('miniuser:login'))

    def test_logout_url(self):
        """Does reverse() return the right url?"""
        self.assertEqual('/logout/', reverse('miniuser:logout'))

    def test_signup_url(self):
        """Does reverse() return the right url?"""
        self.assertEqual('/signup/', reverse('miniuser:signup'))
