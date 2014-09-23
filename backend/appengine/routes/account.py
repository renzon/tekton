# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from pytz import common_timezones
import settings
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse


@login_required
def edit(_logged_user, name, user_locale, timezone):
    if name:
        _logged_user.name = name
    _logged_user.locale = user_locale
    _logged_user.timezone = timezone
    _logged_user.put()
    return RedirectResponse('/')


@login_required
@no_csrf
def index(_logged_user):
    _logged_user.locale = _logged_user.locale or settings.DEFAULT_LOCALE
    _logged_user.timezone = _logged_user.timezone or settings.DEFAULT_TIMEZONE
    context = {'user': _logged_user,
               'timezones': common_timezones,
               'save_path': router.to_path(edit)}
    return TemplateResponse(context, 'permission/account_form.html')