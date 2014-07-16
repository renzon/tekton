# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from course_app import facade
from routes.courses import admin


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)},'courses/admin/form.html')


def save(_handler, course_id=None, **course_properties):
    cmd = facade.save_course_cmd(**course_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'course': cmd.form}

        return TemplateResponse(context, 'courses/admin/form.html')
    _handler.redirect(router.to_path(admin))

