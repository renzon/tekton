# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import permissions
from permission_app.model import ALL_PERMISSIONS_LIST, ADMIN
from tekton import router
from tekton.gae.middleware.json_middleware import JsonResponse


@permissions(ADMIN)
@no_csrf
def index():
    dct = {'list_users_path': router.to_path(list_users),
           'groups': ALL_PERMISSIONS_LIST}
    return TemplateResponse(dct)


@permissions(ADMIN)
def list_users(email_prefix='', cursor=None):
    cmd = facade.find_users_by_email_starting_with(email_prefix, cursor)
    users = cmd.execute().result

    def to_dict(user):
        d = user.to_dict(include=['id', 'email', 'name', 'groups'])
        d['update'] = router.to_path(update, user.key.id())
        return d

    users = [to_dict(u) for u in users]
    cursor_str = cmd.cursor.urlsafe() if cmd.cursor else ''
    next_page = router.to_path(list_users, email_prefix=email_prefix, cursor=cursor_str)
    return JsonResponse({'users': users, 'next_page': next_page, 'more': cmd.more})


@permissions(ADMIN)
def update(user_id, groups):
    facade.update_user_groups(user_id, groups).execute()