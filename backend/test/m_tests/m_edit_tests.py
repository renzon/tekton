# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from m_app.m_model import M
from routes.ms.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        m = mommy.save_one(M)
        template_response = index(m.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        m = mommy.save_one(M)
        old_propeties = m.to_dict()
        redirect_response = save(m.key.id(), c='1.01', b='True', d='1.03', f='1.4', i='5', k='k_string',
                                 time='1/1/2014 01:7:0',
                                 date='1/8/2014')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_m = m.key.get()
        self.assertEquals(Decimal('1.01'), edited_m.c)
        self.assertEquals(True, edited_m.b)
        self.assertEquals(Decimal('1.03'), edited_m.d)
        self.assertEquals(1.4, edited_m.f)
        self.assertEquals(5, edited_m.i)
        self.assertEquals('k_string', edited_m.k)
        self.assertEquals(datetime(2014, 1, 1, 1, 7, 0), edited_m.time)
        self.assertEquals(date(2014, 1, 8), edited_m.date)
        self.assertNotEqual(old_propeties, edited_m.to_dict())

    def test_error(self):
        m = mommy.save_one(M)
        old_properties = m.to_dict()
        template_response = save(m.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['c', 'b', 'd', 'f', 'i', 'k', 'time', 'date']), set(errors.keys()))
        self.assertEqual(old_properties, m.key.get().to_dict())
        self.assert_can_render(template_response)
