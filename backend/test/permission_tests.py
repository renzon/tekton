# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaepermission import facade
from routes.permission import home, admin


class HomeTests(GAETestCase):
    def test_render(self):
        response = home.index()
        self.assert_can_render(response)


class AdminTests(GAETestCase):
    def test_render(self):
        response = admin.index()
        self.assert_can_render(response)

    def test_list_users_empty(self):
        response = admin.list_users()
        self.assert_can_serialize_as_json(response)

    def test_list_users(self):
        email = 'foo@gmail.com'
        facade.save_user_cmd(email).execute()
        response = admin.list_users()
        self.assert_can_serialize_as_json(response)
        self.assertEqual(email, response.context['users'][0]['email'])

    def test_update_user(self):
        email = 'foo@gmail.com'
        facade.save_user_cmd(email).execute()
        user = facade.get_user_by_email(email)()
        self.assertListEqual([''], user.groups)

        ADMIN = 'ADMIN'
        admin.update(str(user.key.id()), [ADMIN])

        user = user.key.get()
        self.assertListEqual([ADMIN], user.groups)

        MANAGER = 'MANAGER'
        admin.update(str(user.key.id()), [ADMIN, MANAGER])

        user = user.key.get()
        self.assertListEqual([ADMIN, MANAGER], user.groups)
