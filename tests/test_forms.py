# -*- coding: utf-8 -*-
"""django-miniuser: Tests for the app's forms

These tests target the code in miniuser/forms.py."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag

# app imports
from miniuser.forms import MiniUserSignUpForm

# app imports
from .utils.testcases import MiniuserTestCase


@tag('forms')
class MiniUserSignUpFormTest(MiniuserTestCase):
    """Tests targeting the SignUpForm"""

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=False)
    def test_exclude_email_field(self):
        """If email is not required, don't show the field on signup"""

        form = MiniUserSignUpForm()
        self.assertNotIn('email', form.fields)

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=True)
    def test_include_email_field(self):
        """If an email address is required, it has to be present during signup"""

        form = MiniUserSignUpForm()
        self.assertIn('email', form.fields)
