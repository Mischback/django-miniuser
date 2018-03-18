# -*- coding: utf-8 -*-
"""django-miniuser: Tests for the app's signal handling

These tests target the code in miniuser/signals.py."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import signals  # noqa
from django.test import tag

# app imports
from miniuser.models import MiniUser

# app imports
from .utils.testcases import MiniuserTestCase

# Python 2/3 compatible import of unittest.mock (or just mock)
# Installation of mock-library is included in tox.ini for 2.7 environments
try:
    from unittest import mock
except ImportError:
    import mock


@tag('signals')
class MiniUserCallbackTests(MiniuserTestCase):
    """Tests targeting the callback functions"""

    @skip('NOT WORKING!!!')
    def test_callback_user_logged_in(self):
        """A successful login updates the timestamp of the user object"""

        with mock.patch('miniuser.signals.callback_user_logged_in') as mock_method:

            u = MiniUser.objects.create_user(username='foo', password='bar')
            self.client.login(username=u.username, password=u.password)

            self.assertEqual(mock_method.call_count, 1)
