# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from course_app import facade
from web import courses


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)})


def save(_handler, course_id=None, **course_properties):
    if course_id:
        cmd = facade.update_course_cmd(course_id, **course_properties)
    else:
        cmd = facade.save_course_cmd(**course_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'course': cmd.form}

        return TemplateResponse(context, 'courses/form.html')
    _handler.redirect(router.to_path(courses))


@no_csrf
def edit(course_id):
    course = facade.get_course_cmd(course_id)()
    context = {'save_path': router.to_path(save, course_id), 'course': facade.detail_course_dct(course)}
    return TemplateResponse(context, 'courses/form.html')

