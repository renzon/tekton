# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import facade
from routes import account
import settings
from tekton.gae.middleware.redirect import RedirectResponse


class AccountTests(GAETestCase):
    def test_index(self):
        email = 'foo@gmail.com'
        user = facade.save_user_cmd(email)()
        response = account.index(user)
        self.assert_can_render(response)

    def test_edit(self):
        email = 'foo@gmail.com'
        initial_name = 'initial_name'
        user = facade.save_user_cmd(email, initial_name)()
        self.assertEqual(initial_name, user.name)
        self.assertEqual(settings.DEFAULT_LOCALE, user.locale)
        self.assertEqual(settings.DEFAULT_TIMEZONE, user.timezone)
        edited_name = 'edited_name'
        locale = 'pt_BR'
        timezone = 'America/Sao_Paulo'
        response = account.edit(user, edited_name, locale, timezone)
        user = user.key.get()
        self.assertIsInstance(response, RedirectResponse)
        self.assertEqual(edited_name, user.name)
        self.assertEqual(locale, user.locale)
        self.assertEqual(timezone, user.timezone)
