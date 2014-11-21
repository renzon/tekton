# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from m_app.m_model import M
from routes.ms.home import index, delete
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(M)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        m = mommy.save_one(M)
        redirect_response = delete(m.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(m.key.get())

