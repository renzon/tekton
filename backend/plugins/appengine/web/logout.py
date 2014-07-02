# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaepermission import facade
from gaepermission.decorator import login_required
from tekton.gae.middleware.redirect import RedirectResponse


@login_required
def index(_resp):
    facade.logout(_resp).execute()
    return RedirectResponse('/')