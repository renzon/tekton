# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from user_app import facade


def index():
    cmd = facade.list_users_cmd()
    user_list = cmd()
    user_short = [facade.short_user_dct(n) for n in user_list]
    return JsonResponse(user_short)


def save(**user_properties):
    cmd = facade.save_user_cmd(**user_properties)
    return _save_or_update_json_response(cmd)


def update(user_id, **user_properties):
    cmd = facade.update_user_cmd(user_id, **user_properties)
    return _save_or_update_json_response(cmd)


def delete(user_id):
    facade.delete_user_cmd(user_id)()


def _save_or_update_json_response(cmd):
    try:
        user = cmd()
    except CommandExecutionException:
        return JsonResponse({'errors': cmd.errors})
    return JsonResponse(facade.detail_user_dct(user))


