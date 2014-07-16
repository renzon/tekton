# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie import facade
from gaecookie.decorator import no_csrf


@no_csrf
def renew():
    facade.renew().execute()
