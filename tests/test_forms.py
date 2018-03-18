# -*- coding: utf-8 -*-
"""django-miniuser: Tests for the app's forms

These tests target the code in miniuser/forms.py."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.forms import ValidationError
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

    @tag('settings')
    @override_settings(
        MINIUSER_DEFAULT_ACTIVE=False,
        MINIUSER_REQUIRE_VALID_EMAIL=False
    )
    def test_respect_default_inactive(self):
        """Respect the app's setting of DEFAULT_ACTIVE = False"""

        form = MiniUserSignUpForm(
            data={
                'username': 'foo',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        u = form.save()
        self.assertFalse(u.is_active)

    @tag('settings')
    @override_settings(
        MINIUSER_DEFAULT_ACTIVE=True,
        MINIUSER_REQUIRE_VALID_EMAIL=False
    )
    def test_respect_default_active(self):
        """Do accounts get created as active?"""

        form = MiniUserSignUpForm(
            data={
                'username': 'foo',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        u = form.save()
        self.assertTrue(u.is_active)

    @tag('settings')
    @override_settings(
        MINIUSER_DEFAULT_ACTIVE=False,
        MINIUSER_REQUIRE_VALID_EMAIL=True
    )
    def test_validation_email_required(self):
        """Form validation ensures, that an email address is provided"""

        form = MiniUserSignUpForm(
            data={
                'username': 'foo',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)

        form = MiniUserSignUpForm(
            data={
                'username': 'foo',
                'password1': 'foo',
                'password2': 'foo',
                'email': ''
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)

        form = MiniUserSignUpForm(
            data={
                'username': 'foo',
                'password1': 'foo',
                'password2': 'foo',
                'email': 'foo@localhost'
            }
        )
        self.assertTrue(form.is_valid())
