# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from user_app import facade
from web import users

@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)})


def save(_handler, user_id=None, **user_properties):

    if user_id:
        cmd = facade.update_user_cmd(user_id, **user_properties)
    else:
        cmd = facade.save_user_cmd(**user_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'user': cmd.form}

        return TemplateResponse(context, 'users/form.html')
    _handler.redirect(router.to_path(users))

@no_csrf
def edit(user_id):
    user = facade.get_user_cmd(user_id)()
    context = {'save_path': router.to_path(save, user_id), 'user': facade.detail_user_dct(user)}
    return TemplateResponse(context, 'users/form.html')

