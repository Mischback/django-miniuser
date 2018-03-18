# -*- coding: utf-8 -*-
"""django-miniuser: Tests for the app's models

These tests target the code in miniuser/models.py."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag

# app imports
from miniuser.exceptions import MiniUserConfigurationException
from miniuser.models import MiniUser

# app imports
from .utils.testcases import MiniuserTestCase

# Python 2/3 compatible import of unittest.mock (or just mock)
# Installation of mock-library is included in tox.ini for 2.7 environments
try:
    from unittest import mock
except ImportError:
    import mock


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

    @mock.patch('django.utils.timezone.now')
    def test_update_last_login(self, mock_now):
        """Should update the field to current timestamp"""

        mock_now.return_value = '2018-03-16 13:37'

        m = MiniUser.objects.create(username='foo')
        m.update_last_login()

        self.assertEqual(m.last_login, '2018-03-16 13:37')

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
