# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
import settings
from routes.login import pending


@login_not_required
@no_csrf
def index(_resp, ret_path='/'):
    user = users.get_current_user()
    if user:
        cmd = facade.login_google(user, _resp).execute()
        if cmd.pending_link:
            pending_path = router.to_path(pending.index, cmd.pending_link.key.id())
            facade.send_passwordless_login_link(user.email(),
                                                settings.APP_URL + pending_path).execute()
            TemplateResponse({'provider': 'Google', 'email': user.email()}, 'login/pending.html')
    return RedirectResponse(ret_path)