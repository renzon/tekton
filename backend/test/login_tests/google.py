# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import facade
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

    @patch('routes.login.google.facade.send_passwordless_login_link')
    def test_google_user_logged_for_already_email_registered_user(self, send_login_mock):
        email = 'foo@gmail.com'
        self.set_current_user(user_email=email)
        facade.save_or_update_passwordless_app_data('id', 'token').execute()
        facade.save_user_cmd(email).execute()
        response = google.index(Mock())
        self.assertEqual(email, send_login_mock.call_args[0][0])
        self.assert_can_render(response)
