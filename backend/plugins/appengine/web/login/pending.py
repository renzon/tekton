# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required


@no_csrf
@login_not_required
def index(_handler, _resp, pending_id, ticket):
    facade.login_checking_email(pending_id, ticket, _resp).execute()
    _handler.redirect('/')