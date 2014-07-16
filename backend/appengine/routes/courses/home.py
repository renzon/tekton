# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from course_app import facade
from routes.courses import admin


@login_not_required
@no_csrf
def index():
    cmd = facade.list_courses_cmd()
    courses = cmd()
    public_form = facade.course_public_form()
    course_public_dcts = [public_form.fill_with_model(course) for course in courses]
    context = {'courses': course_public_dcts,'admin_path':router.to_path(admin)}
    return TemplateResponse(context)

