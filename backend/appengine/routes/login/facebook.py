# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required, permissions
from permission_app.model import ADMIN
import settings
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from routes import admin
from routes.login import pending


@login_not_required
def index(_resp, token, ret_path='/'):
    cmd = facade.login_facebook(token, _resp)
    cmd()
    if cmd.pending_link:
        pending_path = router.to_path(pending.index, cmd.pending_link.key.id())
        user_email = cmd.main_user_from_email.email
        facade.send_passwordless_login_link(user_email,
                                            settings.APP_URL + pending_path).execute()
        return TemplateResponse({'provider': 'Facebook', 'email': user_email}, 'login/pending.html')
    return RedirectResponse(ret_path)

@permissions(ADMIN)
@no_csrf
def form():
    app = facade.get_facebook_app_data().execute().result
    dct = {'save_app_path': router.to_path(save), 'app': app}
    return TemplateResponse(dct)

@permissions(ADMIN)
def save( app_id, token):
    facade.save_or_update_facebook_app_data(app_id, token).execute()
    return RedirectResponse(admin)