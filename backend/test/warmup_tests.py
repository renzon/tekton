# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from routes.warmup import BaseHandler


class BaseTest(GAETestCase):
    def test_warmup_success(self):
        BaseHandler().get()