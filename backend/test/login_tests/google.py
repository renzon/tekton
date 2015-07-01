# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from mock import Mock
from routes.login import google
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_no_google_user_logged(self):
        response = google.index(Mock())
        self.assertIsInstance(response, RedirectResponse)
