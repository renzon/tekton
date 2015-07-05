# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from routes.permission import home, admin


class HomeTests(GAETestCase):
    def test_render(self):
        response = home.index()
        self.assert_can_render(response)


class AdminTests(GAETestCase):
    def test_render(self):
        response = admin.index()
        self.assert_can_render(response)
