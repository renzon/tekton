# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from course_app import course_facade
from routes import courses
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'courses/course_form.html')

@login_not_required
@no_csrf
def save(**course_properties):
    cmd = course_facade.save_course_cmd(**course_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'course': course_properties}

        return TemplateResponse(context, 'courses/course_form.html')
    return RedirectResponse(router.to_path(courses))

