# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from user import facade


def index():
    cmd = facade.list_user()
    user_list = cmd()
    user_short = [facade.short_user(n) for n in user_list]
    return JsonResponse(user_short)


def save(**user_properties):
    cmd = facade.save_user(**user_properties)
    try:
        user = cmd()
    except CommandExecutionException:
        return JsonResponse({'errors': cmd.errors})
    return JsonResponse(facade.detail_user(user))


def update(user_id, **user_properties):
    cmd = facade.update_user(user_id, **user_properties)
    try:
        user = cmd()
    except CommandExecutionException:
        return JsonResponse({'errors': cmd.errors})

    return JsonResponse(facade.detail_user(user))


