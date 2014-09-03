# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api.users import create_logout_url, get_current_user
from gaepermission import facade
from gaepermission.decorator import login_required
from tekton.gae.middleware.redirect import RedirectResponse


@login_required
def index(_resp):
    facade.logout(_resp).execute()
    redirect_url = '/'
    google_user = get_current_user()
    if google_user:
        redirect_url = create_logout_url(redirect_url)
    return RedirectResponse(redirect_url)