# -*- coding: utf-8 -*-
"""miniuser's test base classes"""

# app imports
from ..models import MiniUser, MiniUserManager
from .utils.testcases import MiniuserTestCase


class MiniUserManagetTest(MiniuserTestCase):
    """Tests targeting the MiniUserManager"""

    def test_no_username(self):
        """No user can be created without a username

        Raises a ValueError"""
        manager = MiniUserManager()
        with self.assertRaisesMessage(Exception, 'The username must be set!'):
            m = manager.create_user(None, None)


class MiniUserModelTest(MiniuserTestCase):
    """Tests targeting the actual MiniUser model"""

    def test_string(self):
        """Tests the __str__-method"""
        m = MiniUser.objects.create(username='django')
        self.assertTrue(isinstance(m, MiniUser))
        self.assertEqual(m.__str__(), m.username)
