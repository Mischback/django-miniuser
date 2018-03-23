# -*- coding: utf-8 -*-
"""django-miniuser: Tests for the admin interface

These tests target the code in miniuser/admin.py."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.admin import ModelAdmin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.test import override_settings, tag
from django.test.client import RequestFactory
from django.urls import reverse

# app imports
from miniuser.admin import MiniUserAdmin, MiniUserAdminStaffStatusFilter
from miniuser.models import MiniUser

# app imports
from .utils.testcases import MiniuserTestCase


@tag('admin')
class MiniUserAdminStaffStatusFilterTest(MiniuserTestCase):
    """Tests the custom filter"""

    def test_staff_status_filter(self):
        """Returned queryset matches the specified parameter"""

        # create objects
        su = MiniUser.objects.create(username='superuser', is_staff=True, is_superuser=True)
        s = MiniUser.objects.create(username='staff_user', is_staff=True)
        u = MiniUser.objects.create(username='user')

        f = MiniUserAdminStaffStatusFilter(None, {'status': 'superusers'}, MiniUser, MiniUserAdmin)
        f_result = f.queryset(None, MiniUser.objects.all())
        # expected result: only the superuser (su)
        self.assertEqual(f_result[0], su)
        # and no more than this one superuser (su)
        with self.assertRaises(IndexError):
            self.assertEqual(f_result[1], True)

        f = MiniUserAdminStaffStatusFilter(None, {'status': 'staff'}, MiniUser, MiniUserAdmin)
        f_result = f.queryset(None, MiniUser.objects.all())
        # expected result: the superuser (su) and the staff_user (s)
        self.assertEqual(f_result[0], su)
        self.assertEqual(f_result[1], s)
        # and no more than this two
        with self.assertRaises(IndexError):
            self.assertEqual(f_result[2], True)

        f = MiniUserAdminStaffStatusFilter(None, {'status': 'users'}, MiniUser, MiniUserAdmin)
        f_result = f.queryset(None, MiniUser.objects.all())
        # expected result: only the user (u)
        self.assertEqual(f_result[0], u)
        # and no more than this one user (u)
        with self.assertRaises(IndexError):
            self.assertEqual(f_result[1], True)

        f = MiniUserAdminStaffStatusFilter(None, {}, MiniUser, MiniUserAdmin)
        f_result = f.queryset(None, MiniUser.objects.all())
        # expected result: the superuser (su) and the staff_user (s)
        self.assertEqual(f_result[0], su)
        self.assertEqual(f_result[1], s)
        self.assertEqual(f_result[2], u)
        # and no more than this two
        with self.assertRaises(IndexError):
            self.assertEqual(f_result[3], True)


@tag('admin')
class MiniUserAdminChangeListTest(MiniuserTestCase):
    """Tests the custom ModelAdmin"""

    def setUp(self):
        """Prepare the tests"""

        self.site = AdminSite()

    def test_status_aggregated(self):
        """MiniUser-objects' status is correctly evaluated"""

        ma = MiniUserAdmin(MiniUser, self.site)
        u = MiniUser.objects.create(username='user')

        self.assertEqual(ma.status_aggregated(u), 'user')

        u.is_staff = True
        self.assertEqual(ma.status_aggregated(u), 'staff')

        u.is_superuser = True
        self.assertEqual(ma.status_aggregated(u), 'superuser')

    @tag('miniuser_settings', 'admin_settings')
    @override_settings(
        MINIUSER_ADMIN_STATUS_COLOR_STAFF='#f0f0f0',
        MINIUSER_ADMIN_STATUS_COLOR_SUPERUSER='#0f0f0f'
    )
    def test_username_color_status(self):
        """Usernames are colored depending on the user's status"""

        ma = MiniUserAdmin(MiniUser, self.site)
        u = MiniUser.objects.create(username='user')

        self.assertEqual(ma.username_color_status(u), u.username)

        u.is_staff = True
        self.assertEqual(
            ma.username_color_status(u),
            '<span style="color: {};">{}</span>'.format('#f0f0f0', u.username)
        )

        u.is_superuser = True
        self.assertEqual(
            ma.username_color_status(u),
            '<span style="color: {};">{}</span>'.format('#0f0f0f', u.username)
        )

    @tag('miniuser_settings', 'admin_settings')
    @override_settings(
        MINIUSER_ADMIN_STATUS_CHAR_STAFF='a',
        MINIUSER_ADMIN_STATUS_CHAR_SUPERUSER='b'
    )
    def test_username_character_status(self):
        """Usernames are decorated depending on the user's status"""

        ma = MiniUserAdmin(MiniUser, self.site)
        u = MiniUser.objects.create(username='user')

        self.assertEqual(ma.username_character_status(u), u.username)

        u.is_staff = True
        self.assertEqual(ma.username_character_status(u), '[{}] {}'.format('a', u.username))

        u.is_superuser = True
        self.assertEqual(ma.username_character_status(u), '[{}] {}'.format('b', u.username))

    def test_email_with_status(self):
        """Combines email address with email verification status"""

        ma = MiniUserAdmin(MiniUser, self.site)
        u = MiniUser.objects.create(username='user', email='user@localhost')

        self.assertEqual(ma.email_with_status(u), '{} {}'.format(_boolean_icon(u.email_is_verified), u.email))

    @tag('miniuser_settings', 'admin_settings')
    @override_settings(
        MINIUSER_ADMIN_LIST_DISPLAY=['username_color_status'],
        MINIUSER_ADMIN_STATUS_COLOR_STAFF='#f0f0f0',
        MINIUSER_ADMIN_STATUS_COLOR_SUPERUSER='#0f0f0f'
    )
    def test_get_legend_color(self):
        """Returns the legend for colored usernames"""

        ma = MiniUserAdmin(MiniUser, self.site)
        self.assertEqual(ma.get_miniuser_legend(), {'color': {'superuser': '#0f0f0f', 'staff': '#f0f0f0'}})

    @tag('miniuser_settings', 'admin_settings')
    @override_settings(
        MINIUSER_ADMIN_LIST_DISPLAY=['username_character_status'],
        MINIUSER_ADMIN_STATUS_CHAR_STAFF='a',
        MINIUSER_ADMIN_STATUS_CHAR_SUPERUSER='b'
    )
    def test_get_legend_character(self):
        """Returns the legend for character status decorated usernames"""

        ma = MiniUserAdmin(MiniUser, self.site)
        self.assertEqual(ma.get_miniuser_legend(), {'character': {'superuser': 'b', 'staff': 'a'}})

    @tag('miniuser_settings', 'admin_settings')
    @override_settings(
        MINIUSER_ADMIN_LIST_DISPLAY=['username_color_status', 'username_character_status'],
        MINIUSER_ADMIN_STATUS_COLOR_STAFF='#f0f0f0',
        MINIUSER_ADMIN_STATUS_COLOR_SUPERUSER='#0f0f0f',
        MINIUSER_ADMIN_STATUS_CHAR_STAFF='a',
        MINIUSER_ADMIN_STATUS_CHAR_SUPERUSER='b'
    )
    def test_get_legend_both(self):
        """Returns both legends"""

        ma = MiniUserAdmin(MiniUser, self.site)
        result = ma.get_miniuser_legend()
        self.assertEqual(result['character'], {'superuser': 'b', 'staff': 'a'})
        self.assertEqual(result['color'], {'superuser': '#0f0f0f', 'staff': '#f0f0f0'})

    def test_get_actions_raw(self):
        """Directly tests the get_actions()-method"""

        factory = RequestFactory()
        request = factory.get(reverse('admin:miniuser_miniuser_changelist'))
        ma = MiniUserAdmin(MiniUser, self.site)
        modeladmin = ModelAdmin(MiniUser, self.site)

        actions = modeladmin.get_actions(request)
        self.assertIn('delete_selected', actions)

        actions = ma.get_actions(request)
        self.assertNotIn('delete_selected', actions)


class MiniUserAdminActionsTest(MiniuserTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = MiniUser.objects.create_superuser(
            username='django',
            password='django',
            email='django@localhost'
        )

    def setUp(self):
        self.client.force_login(self.superuser)

    def test_get_actions(self):
        """Delete User objects should not be available

        So, this test is working, but it does not really cover the source of
        get_actions()."""

        response = self.client.get(reverse('admin:miniuser_miniuser_changelist'))
        self.assertNotContains(response, 'delete_selected')

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=False)
    def test_action_bulk_activate_single_user(self):
        """Activate a single user by drop down"""

        u = MiniUser.objects.create(username='user', is_active=False)
        v = MiniUser.objects.create(username='foo', is_active=False)
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk],
            'action': 'action_bulk_activate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # user 'user' is active
        self.assertTrue(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'The user {} was activated successfully.'.format(u.username))

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=False)
    def test_action_bulk_activate_multiple_users(self):
        """Activate multiple users by drop down"""

        u = MiniUser.objects.create(username='user', is_active=False)
        v = MiniUser.objects.create(username='foo', is_active=False)
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # try to activate two users
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk, v.pk],
            'action': 'action_bulk_activate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # both users are active
        self.assertTrue(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertTrue(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates the activation of 2 users
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]), '{} users were activated successfully ({}, {}).'.format(2, v.username, u.username)
        )

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=True)
    def test_action_bulk_activate_single_user_verified_mail(self):
        """Activate a single user by drop down without verified email"""

        u = MiniUser.objects.create(username='user', is_active=False)
        v = MiniUser.objects.create(username='foo', is_active=False)
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk],
            'action': 'action_bulk_activate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # user 'user' is not actived
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates, that the user could not be activated
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'The user {} could not be activated, because his email address is not verified!'.format(u.username)
        )

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=True)
    def test_action_bulk_activate_multiple_users_verified_mail(self):
        """Activate multiple users by drop down without verified email"""

        u = MiniUser.objects.create(username='user', is_active=False)
        v = MiniUser.objects.create(username='foo', is_active=False)
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # try to activate two users
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk, v.pk],
            'action': 'action_bulk_activate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # both users remain inactive
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates the activation of 2 users
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            '{} users could not be activated, because their email addresses are not verified ({}, {})!'.format(
                2, v.username, u.username
            )
        )

    @skip('NOT WORKING')
    def test_action_bulk_activate_invalid_user(self):
        """Don't activate invalid user"""

        u = MiniUser.objects.create(username='user', is_active=False)
        v = MiniUser.objects.create(username='foo', is_active=False)
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # try to activate an invalid user
        # TODO: This is not working, no valid queryset is constructed
        action_data = {
            ACTION_CHECKBOX_NAME: [999],
            'action': 'action_bulk_activate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # no user is activated
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates, that the corresponding user could not be found
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'No User object with the given ID ({}) found!'.format(999)
        )

    @skip('NOT WORKING')
    def test_action_bulk_activate_invalid_users(self):
        """Don't activate invalid users"""

        u = MiniUser.objects.create(username='user', is_active=False)
        v = MiniUser.objects.create(username='foo', is_active=False)
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # try to activate two invalid users
        # TODO: This is not working, no valid queryset is constructed
        action_data = {
            ACTION_CHECKBOX_NAME: [999, 998],
            'action': 'action_bulk_activate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # no user is activated
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates, that the corresponding users could not be found
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'No User objects with the given IDs found ({}, {})!'.format(998, 999)
        )

    @override_settings(MINIUSER_REQUIRE_VALID_EMAIL=False)
    def test_action_activate_user(self):
        """Activate a single user by button (pass to bulk method)

        Additionally tests invalid user IDs."""

        m = MiniUser.objects.create(username='foo', is_active=False)

        response = self.client.get(reverse('admin:miniuser-activate-user', args=[m.pk]))

        # the local reference doesn't get updated. So fetch the user again...
        n = MiniUser.objects.get(pk=m.pk)
        self.assertTrue(n.is_active)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'The user {} was activated successfully.'.format(n.username))
        self.assertRedirects(response, reverse('admin:miniuser_miniuser_changelist'))

        response = self.client.get(reverse('admin:miniuser-activate-user', args=[999]))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'No User object with the given ID ({}) found!'.format(999))

    def test_action_bulk_deactivate_single_user(self):
        """Deactivate a single user by drop down"""

        u = MiniUser.objects.create(username='user', is_active=True)
        v = MiniUser.objects.create(username='foo', is_active=True)
        self.assertTrue(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertTrue(MiniUser.objects.get(pk=v.pk).is_active)

        # try to deactivate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk],
            'action': 'action_bulk_deactivate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # user 'user' is deactived
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertTrue(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'The user {} was deactivated successfully.'.format(u.username))

    def test_action_bulk_deactivate_multiple_users(self):
        """Deactivate multiple users by drop down"""

        u = MiniUser.objects.create(username='user', is_active=True)
        v = MiniUser.objects.create(username='foo', is_active=True)
        self.assertTrue(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertTrue(MiniUser.objects.get(pk=v.pk).is_active)

        # try to deactivate two users
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk, v.pk],
            'action': 'action_bulk_deactivate_user',
        }
        response = self.client.post(reverse('admin:miniuser_miniuser_changelist'), action_data, follow=True)

        # both users are deactived
        self.assertFalse(MiniUser.objects.get(pk=u.pk).is_active)
        self.assertFalse(MiniUser.objects.get(pk=v.pk).is_active)

        # message indicates the activation of 2 users
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]), '{} users were deactivated successfully ({}, {}).'.format(2, v.username, u.username)
        )

    def test_action_bulk_deactivate_invalid_user(self):
        """Don't deactivate invalid user"""
        pass

    def test_action_bulk_deactivate_invalid_users(self):
        """Don't deactivate invalid users"""
        pass

    @tag('current')
    def test_action_deactivate_user(self):
        """Deactivate a single user by button (pass to bulk method)"""

        m = MiniUser.objects.create(username='foo', is_active=True)

        response = self.client.get(reverse('admin:miniuser-deactivate-user', args=[m.pk]))

        # the local reference doesn't get updated. So fetch the user again...
        n = MiniUser.objects.get(pk=m.pk)
        self.assertFalse(n.is_active)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'The user {} was deactivated successfully.'.format(n.username))
        self.assertRedirects(response, reverse('admin:miniuser_miniuser_changelist'))

        response = self.client.get(reverse('admin:miniuser-deactivate-user', args=[999]))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'No User object with the given ID ({}) found!'.format(999))

    @tag('current')
    def test_action_deactivate_own_account(self):

        response = self.client.get(reverse('admin:miniuser-deactivate-user', args=[self.superuser.pk]))
        self.assertTrue(MiniUser.objects.get(pk=self.superuser.pk).is_active)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'The user {} could not be deactivated, because this is your own account!'.format(self.superuser.username)
        )
