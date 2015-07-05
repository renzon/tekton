# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from mock import patch
from routes.login import passwordless
from routes.login.passwordless import check
import settings
from tekton.router import to_path


class IndexTests(GAETestCase):
    def test_success(self):
        response = passwordless.index()
        self.assert_can_render(response)


class SendEmailTests(GAETestCase):
    @patch('routes.login.passwordless.facade.send_passwordless_login_link')
    def test_success(self, send_link_mock):
        email = 'foo@bar.com'
        passwordless.send_email(email)
        send_link_mock.assert_called_once_with(email,
                                               settings.APP_URL + to_path(check, ret_path='/'))
