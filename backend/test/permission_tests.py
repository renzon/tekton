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
        facade.save_user_cmd('foo@gmail.com')
        response = admin.list_users()
        self.assert_can_serialize_as_json(response)
