# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from webapp2_extras import i18n
from tekton.gae.middleware import Middleware


class LocaleMiddleware(Middleware):
    def set_up(self):
        if 'locale' in self.request_args or 'fb_locale' in self.request_args:
            locale = self.request_args.get('locale', '')
            # fucking Facebook scrapper sending undesired params
            locale = locale or self.request_args.get('fb_locale', '')
            print 'Locale ' + locale
            del self.request_args['locale']
            if locale:
                locale_obj = i18n.get_i18n()
                locale_obj.set_locale(locale)
                if locale == 'pt_BR':
                    locale_obj.set_timezone('America/Sao_Paulo')