# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from mock import patch, Mock
from routes.login import passwordless
from routes.login.passwordless import check
import settings
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


class IndexTests(GAETestCase):
    def test_success(self):
        response = passwordless.index()
        self.assert_can_render(response)


class FormTests(GAETestCase):
    def test_render(self):
        response = passwordless.form()
        self.assert_can_render(response)


class SendEmailTests(GAETestCase):
    @patch('routes.login.passwordless.facade.send_passwordless_login_link')
    def test_success(self, send_link_mock):
        email = 'foo@bar.com'
        passwordless.send_email(email)
        send_link_mock.assert_called_once_with(email,
                                               settings.APP_URL + to_path(check, ret_path='/'))


class CheckEmailTests(GAETestCase):
    @patch('routes.login.passwordless.facade.login_passwordless')
    def test_success(self, login_mock):
        http_resp = Mock()
        ticket = 'ticket'
        cmd_mock = Mock()
        login_mock.return_value = cmd_mock
        response = passwordless.check(http_resp, ticket)
        self.assertIsInstance(response, RedirectResponse)
        login_mock.assert_called_once_with(ticket, http_resp)
        cmd_mock.execute.assert_called_once_with()
