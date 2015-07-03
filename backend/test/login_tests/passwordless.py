# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from routes.login import passwordless


class IndexTests(GAETestCase):
    def test_success(self):
        response = passwordless.index()
        self.assert_can_render(response)
