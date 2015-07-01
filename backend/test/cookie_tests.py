# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gaecookie import facade
from routes.cookie.tasks import renew


class RenewTests(GAETestCase):
    def test_success(self):
        signed = facade.sign('foo', 'bar')()
        renew()
        signed_after_renew = facade.sign('foo', 'bar')()
        self.assertNotEqual(signed, signed_after_renew)
