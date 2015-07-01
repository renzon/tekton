# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from routes.admin.home import index


class HomeTests(GAETestCase):
    def test_index(self):
        response = index()
        self.assert_can_render(response)
