# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from user import facade


def save(**n_properties):
    cmd = facade.save_n(**n_properties)
    try:
        n = cmd()
    except CommandExecutionException:
        return JsonResponse({'errors': cmd.errors})
    return JsonResponse(facade.localize_n(n))


def update(n_id, **n_properties):
    cmd = facade.update_n(n_id, **n_properties)
    try:
        n = cmd()
    except CommandExecutionException:
        return JsonResponse({'errors': cmd.errors})

    return JsonResponse(facade.localize_n(n))


