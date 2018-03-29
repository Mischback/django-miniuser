# -*- coding: utf-8 -*-
"""django-miniuser: Tests for the app's models

These tests target the code in miniuser/models.py."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag

# app imports
from miniuser.exceptions import (
    MiniUserConfigurationException, MiniUserObjectActionException,
)
from miniuser.models import MiniUser

# app imports
from .utils.testcases import MiniuserTestCase


@tag('model')
class MiniUserManagerTest(MiniuserTestCase):
    """Tests targeting the MiniUserManager"""

    @tag('miniuser_settings')
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

    @tag('miniuser_settings')
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

    @tag('miniuser_settings')
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

    @tag('miniuser_settings')
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

    @tag('miniuser_settings')
    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=False)
    def test_no_email_allowed(self):
        """If users require a email address is controlled by app specific setting

        MINIUSER_REQUIRE_VALID_EMAIL = False, so the user should be created
        without email address"""
        m = MiniUser.objects.create_user('foo')

        self.assertFalse(m.email)
        self.assertEqual(m.email, None)

    @tag('miniuser_settings')
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

    @tag('miniuser_settings')
    @override_settings(MINIUSER_LOGIN_NAME='username')
    def test_natural_key_username(self):
        """Get a user by its username

        The user is retrieved by its username and is not retrievable by its
        mail address."""
        m = MiniUser.objects.create_user(username='foo', email='foo@bar.com')
        self.assertEqual(m, MiniUser.objects.get_by_natural_key('foo'))
        with self.assertRaises(MiniUser.DoesNotExist):
            n = MiniUser.objects.get_by_natural_key('foo@bar.com') # noqa

    @tag('miniuser_settings')
    @override_settings(MINIUSER_LOGIN_NAME='email')
    def test_natural_key_email(self):
        """Get a user by its email address

        The user is retrieved by its email address and is not retrievable by its
        username."""
        m = MiniUser.objects.create_user(username='foo', email='foo@bar.com')
        self.assertEqual(m, MiniUser.objects.get_by_natural_key('foo@bar.com'))
        with self.assertRaises(MiniUser.DoesNotExist):
            n = MiniUser.objects.get_by_natural_key('foo') # noqa

    @tag('miniuser_settings')
    @override_settings(MINIUSER_LOGIN_NAME='both')
    def test_natural_key_both(self):
        """Get a user by its username or email address

        The user is retrieved by its username and its email address."""
        m = MiniUser.objects.create_user(username='foo', email='foo@bar.com')
        self.assertEqual(m, MiniUser.objects.get_by_natural_key('foo'))
        self.assertEqual(m, MiniUser.objects.get_by_natural_key('foo@bar.com'))

    @tag('miniuser_settings')
    @override_settings(MINIUSER_LOGIN_NAME='foo')
    def test_natural_key_invalid(self):
        """Raises an exception, if MINIUSER_LOGIN_NAME has undefined value

        This is an absolute safe-guard, because the parameters are checked with
        Django's check-framework (see apps.py:check_correct_values() and
        models.py.

        To be completely honest: This was introduced to reach 100% coverage."""
        with self.assertRaisesMessage(MiniUserConfigurationException, "'MINIUSER_LOGIN_NAME' has an undefined value!"):
            n = MiniUser.objects.get_by_natural_key('foo') # noqa


@tag('model')
class MiniUserModelTest(MiniuserTestCase):
    """Tests targeting the actual MiniUser model"""

    def test_fix_empty_email(self):
        """Empty email should be cleaned to 'None'"""

        m = MiniUser.objects.create(username='foo', email='')
        m.clean()
        self.assertNotEqual(m.email, '')
        self.assertEqual(m.email, None)

        n = MiniUser.objects.create(username='bar', email='valid@localhost')
        n.clean()
        self.assertNotEqual(n.email, '')
        self.assertNotEqual(n.email, None)
        self.assertEqual(n.email, 'valid@localhost')

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=False)
    def test_activate_user(self):
        """Inactive user object should be activated"""

        m = MiniUser.objects.create(username='foo', is_active=False)
        m.activate_user()
        self.assertTrue(m.is_active)

        # do nothing, if the user is already active
        n = MiniUser.objects.create(username='bar', is_active=True)
        n.activate_user()
        self.assertTrue(n.is_active)

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=True)
    def test_activate_user_require_mail(self):
        """asdf"""

        m = MiniUser.objects.create(username='foo', is_active=False, email_is_verified=True)
        m.activate_user()
        self.assertTrue(m.is_active)

        # raise exception without verified email
        n = MiniUser.objects.create(username='bar', email_is_verified=False)
        with self.assertRaisesMessage(
            MiniUserObjectActionException,
                'You tried to activate an User-object, that has no '
                'verified email address, but your project requires the '
                'verification of email addresses.'
        ):
            n.activate_user()  # noqa

    def test_deactivate_user(self):
        """Active user objects should be deactivated"""

        m = MiniUser.objects.create(username='foo', is_active=True)
        m.deactivate_user()
        self.assertFalse(m.is_active)

        # do nothing, if the user is already deactivated
        n = MiniUser.objects.create(username='bar', is_active=False)
        n.deactivate_user()
        self.assertFalse(n.is_active)

        # don't deactivate the requesting user
        o = MiniUser.objects.create(username='asdf', is_active=False)
        with self.assertRaisesMessage(MiniUserObjectActionException, 'You can not deactivate yourself.'):
            o.deactivate_user(o)  # noqa
