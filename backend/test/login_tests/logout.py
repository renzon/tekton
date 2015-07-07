# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from mock import Mock
from routes import logout
from tekton.gae.middleware.redirect import RedirectResponse


class LogoutTests(GAETestCase):
    def test_logout_without_logged_google_user(self):
        response = logout.index(Mock())
        self.assertIsInstance(response, RedirectResponse)
        self.assertEqual('/', response.context)

    def test_logout_with_logged_google_user(self):
        self.set_current_user()
        response = logout.index(Mock())
        self.assertIsInstance(response, RedirectResponse)
        self.assertEqual('https://www.google.com/accounts/Logout?continue=http%3A//testbed.example.com/', response.context)
