# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.json_middleware import JsonResponse
from course_app import course_facade

@login_not_required
@no_csrf
def index():
    cmd = course_facade.list_courses_cmd()
    course_list = cmd()
    course_form=course_facade.course_form()
    course_dcts = [course_form.fill_with_model(m) for m in course_list]
    return JsonResponse(course_dcts)

@login_not_required
@no_csrf
def new(_resp, **course_properties):
    cmd = course_facade.save_course_cmd(**course_properties)
    return _save_or_update_json_response(cmd, _resp)

@login_not_required
@no_csrf
def edit(_resp, course_id, **course_properties):
    cmd = course_facade.update_course_cmd(course_id, **course_properties)
    return _save_or_update_json_response(cmd, _resp)

@login_not_required
@no_csrf
def delete(course_id):
    course_facade.delete_course_cmd(course_id)()

@login_not_required
@no_csrf
def _save_or_update_json_response(cmd, _resp):
    try:
        course = cmd()
    except CommandExecutionException:
        _resp.status_code = 400
        return JsonResponse({'errors': cmd.errors})
    course_form=course_facade.course_form()
    return JsonResponse(course_form.fill_with_model(course))

