# -*- coding: utf-8 -*-
"""miniuser's test base classes"""

# Python imports
from unittest import skip # noqa

# Django imports
from django.test import override_settings

# app imports
from ..models import MiniUser
from .utils.testcases import MiniuserTestCase


class MiniUserManagerTest(MiniuserTestCase):
    """Tests targeting the MiniUserManager"""

    @override_settings(MINIUSER_DEFAULT_ACTIVE=True)
    def test_create_user_without_password(self):
        """Are fields populated while keeping the user inactive (lacking pw)?

        A new MiniUser object will be created, but it does not have a usable
        password. So, instead of applying the app's setting, to activate all
        newly created users, the user is not activated because of his lacking
        password."""
        m = MiniUser.objects.create_user('foo', email='foo@BAR.COM')
        self.assertEqual(m.username, 'foo')
        self.assertEqual(m.email, 'foo@bar.com')
        self.assertFalse(m.has_usable_password())
        self.assertFalse(m.is_active)

    @override_settings(MINIUSER_DEFAULT_ACTIVE=True)
    def test_create_user_with_password(self):
        """Are the fields populated, including the activation of the user?

        The new MiniUser will have 'is_active' = True, because a password is
        provided."""
        m = MiniUser.objects.create_user('foo', email='foo@BAR.CoM', password='superpassword')
        self.assertEqual(m.username, 'foo')
        self.assertEqual(m.email, 'foo@bar.com')
        self.assertTrue(m.has_usable_password())
        self.assertTrue(m.is_active)

    @override_settings(MINIUSER_DEFAULT_ACTIVE=False)
    def test_create_user_without_activation(self):
        """Are the fields populated without activating the user?

        The new MiniUser will have 'is_active' = False, though everything is
        provided as needed. The method applies the app specific setting
        MINIUSER_DEFAULT_ACTIVE = False."""
        m = MiniUser.objects.create_user('foo', email='foo@BAR.CoM', password='superpassword')
        self.assertEqual(m.username, 'foo')
        self.assertEqual(m.email, 'foo@bar.com')
        self.assertTrue(m.has_usable_password())
        self.assertFalse(m.is_active)

    @override_settings(MINIUSER_DEFAULT_ACTIVE=False)
    def test_create_user_respect_activation_setting(self):
        """Are the fields populated without activating the user?

        It should not be possible to bypass the MINIUSER_DEFAULT_ACTIVE setting,
        should it?"""
        m = MiniUser.objects.create_user(
            'foo',
            email='foo@BAR.CoM',
            password='superpassword',
            is_active=True
        )
        self.assertEqual(m.username, 'foo')
        self.assertEqual(m.email, 'foo@bar.com')
        self.assertTrue(m.has_usable_password())
        self.assertFalse(m.is_active)

    def test_no_username(self):
        """No user can be created without a username

        Raises a ValueError"""
        with self.assertRaisesMessage(ValueError, 'The username must be set!'):
            m = MiniUser.objects.create_user(None) # noqa

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=False)
    def test_no_email_allowed(self):
        """If users require a email address is controlled by app specific setting

        MINIUSER_REQUIRE_VALID_EMAIL = False, so the user should be created
        without email address"""
        m = MiniUser.objects.create_user('foo')
        # actually m.email is a blank string
        self.assertFalse(m.email)
        self.assertEqual(m.email, '')

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=True)
    def test_no_email_forbidden(self):
        """If users require an email address is controlled by app specific setting

        MINIUSER_REQUIRE_VALID_EMAIL = True, so a ValueError should be raised"""
        with self.assertRaisesMessage(ValueError, 'The email address must be set!'):
            m = MiniUser.objects.create_user('foo') # noqa

    def test_superuser_creation(self):
        """Is the superuser created as needed?

        Basically like any user, but with some extra flags set to True. Please
        note, that an email is required for superusers regardless of the
        app specific MINIUSER_REQUIRE_VALID_EMAIL."""
        m = MiniUser.objects.create_superuser('foo', email='foo@BAR.CoM', password='superpassword')
        self.assertEqual(m.username, 'foo')
        self.assertEqual(m.email, 'foo@bar.com')
        self.assertTrue(m.has_usable_password())
        self.assertTrue(m.is_active)
        self.assertTrue(m.is_staff)
        self.assertTrue(m.is_superuser)


class MiniUserModelTest(MiniuserTestCase):
    """Tests targeting the actual MiniUser model"""

    def test_string(self):
        """Tests the __str__-method"""
        m = MiniUser.objects.create(username='django')
        self.assertTrue(isinstance(m, MiniUser))
        self.assertEqual(m.__str__(), m.username)
