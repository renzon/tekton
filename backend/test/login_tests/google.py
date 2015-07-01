# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from mock import Mock, patch
from routes.login import google
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_no_google_user_logged(self):
        response = google.index(Mock())
        self.assertIsInstance(response, RedirectResponse)

    @patch('routes.login.google.facade')
    def test_google_user_logged(self, facade_mock):
        self.set_current_user()
        cmd_mock = Mock()
        cmd_mock.pending_link = False
        execute_mock = Mock()
        execute_mock.execute = Mock(return_value=cmd_mock)
        facade_mock.login_google = Mock(return_value=execute_mock)
        response = google.index(Mock())
        self.assertIsInstance(response, RedirectResponse)
