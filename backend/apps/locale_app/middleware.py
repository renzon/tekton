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
                import settings  # this is here to avoid cyclic dependency

                locale_obj.set_timezone(settings.DEFAULT_TIMEZONE)
                return True

    def set_up(self):
        handled = self._handle('locale')
        # fucking Facebook scrapper sending undesired param
        handled = self._handle('fb_locale') or handled
        user = self.dependencies['_logged_user']
        import settings  # this is here to avoid cyclic dependency

        if user:
            locale_obj = i18n.get_i18n()
            locale_obj.set_locale(user.locale or settings.DEFAULT_LOCALE)
            locale_obj.set_timezone(user.timezone or settings.DEFAULT_TIMEZONE)
        elif not handled:
            locale_obj = i18n.get_i18n()
            locale_obj.set_locale(settings.DEFAULT_LOCALE)
            locale_obj.set_timezone(settings.DEFAULT_TIMEZONE)


