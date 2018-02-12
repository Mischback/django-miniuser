# -*- coding: utf-8 -*-
"""miniuser's test base classes"""

# app imports
from .utils.testcases import MiniuserTestCase


class WorkingTest(MiniuserTestCase):
    """Just a simple test, to make testing work"""

    def test_working(self):
        """Just returns a test fail.
        This is used to determine, if the test setup is working."""

        self.fail('This should be failing!')
