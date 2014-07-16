# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from course_app import facade
from routes.courses import admin


@no_csrf
def index(course_id):
    course = facade.get_course_cmd(course_id)()
    detail_form = facade.course_detail_form()
    context = {'save_path': router.to_path(save, course_id), 'course': detail_form.fill_with_model(course)}
    return TemplateResponse(context, 'courses/admin/form.html')


def save(_handler, course_id, **course_properties):
    cmd = facade.update_course_cmd(course_id, **course_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'course': cmd.form}

        return TemplateResponse(context, 'courses/admin/form.html')
    _handler.redirect(router.to_path(admin))

