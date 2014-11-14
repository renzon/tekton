# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie import facade
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required


@login_not_required
@no_csrf
def renew():
    facade.renew().execute()
