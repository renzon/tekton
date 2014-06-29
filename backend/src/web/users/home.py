# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from tekton import router
from user import facade
from web.users import form


def delete(_handler, user_id):
    facade.delete_user(user_id)()
    _handler.redirect(router.to_path(index))


def index():
    cmd = facade.list_users()
    users = cmd()
    form_edit_path = router.to_path(form.edit)
    delete_path = router.to_path(delete)

    def short_user_dict(user):
        user_dct = facade.short_user(user)
        user_dct['edit_path'] = '/'.join([form_edit_path, user_dct['id']])
        user_dct['delete_path'] = '/'.join([delete_path, user_dct['id']])
        return user_dct

    short_users = [short_user_dict(user) for user in users]
    context = {'app': 'user',
               'users': short_users,
               'user_form': router.to_path(form)}
    return TemplateResponse(context)