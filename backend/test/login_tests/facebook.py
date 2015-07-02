# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import facade
from mock import Mock, patch
from routes.login import google, facebook
import settings
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    @patch('routes.login.facebook.facade')
    def test_facebook_login(self, facade_mock):
        cmd_mock = Mock()
        cmd_mock.pending_link = False
        facade_mock.login_facebook = Mock(return_value=cmd_mock)
        response = facebook.index(Mock(), 'token')
        self.assertIsInstance(response, RedirectResponse)

    @patch('routes.login.facebook.facade.login_facebook')
    @patch('routes.login.facebook.facade.send_passwordless_login_link')
    def test_facebook_login_for_already_email_registered_user(self, send_login_mock, login_facebook_mock):
        email = 'foo@gmail.com'
        cmd_mock = Mock()
        cmd_mock.main_user_from_email.email = email
        login_facebook_mock.return_value = cmd_mock
        token = 'token'
        facade.save_or_update_passwordless_app_data('id', token).execute()
        facade.save_user_cmd(email).execute()
        resp_mock = Mock()
        response = facebook.index(resp_mock, token)
        login_facebook_mock.assert_called_once_with(token, resp_mock)
        self.assertEqual(email, send_login_mock.call_args[0][0])
        self.assert_can_render(response)


class FormTests(GAETestCase):
    def test_success(self):
        response = facebook.form()
        self.assert_can_render(response)


class SaveTests(GAETestCase):
    def test_success(self):
        app_id = 'app_id'
        token = 'token'
        response=facebook.save(app_id, token)
        self.assertIsInstance(response,RedirectResponse)
