# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from webapp2_extras import i18n
from tekton.gae.middleware import Middleware


class LocaleMiddleware(Middleware):
    def _handle(self, locale_key):
        if locale_key in self.request_args:
            locale = self.request_args.get(locale_key, '')
            print 'Locale ' + locale_key

            self.request_args.pop(locale_key)
            if locale:
                locale_obj = i18n.get_i18n()
                locale_obj.set_locale(locale)
                if locale == 'pt_BR':
                    locale_obj.set_timezone('America/Sao_Paulo')

    def set_up(self):
        self._handle('locale')
        # fucking Facebook scrapper sending undesired param
        self._handle('fb_locale')
