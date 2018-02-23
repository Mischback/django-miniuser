# -*- coding: utf-8 -*-
"""miniuser's test base classes"""

# Python imports
from unittest import skip # noqa

# Django imports
from django.test import override_settings
from django.contrib.admin.sites import AdminSite

# app imports
from .utils.testcases import MiniuserTestCase
from ..models import MiniUser
from ..admin import MiniUserAdminStaffStatusFilter, MiniUserAdmin


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


class MiniUserAdminTest(MiniuserTestCase):
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
        self.assertEqual(
            ma.username_character_status(u), '[{}] {}'.format('a', u.username))

        u.is_superuser = True
        self.assertEqual(
            ma.username_character_status(u), '[{}] {}'.format('b', u.username))
