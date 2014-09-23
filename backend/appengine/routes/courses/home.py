# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from course_app import course_facade
from routes.courses import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index():
    cmd = course_facade.list_courses_cmd()
    courses = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    course_form = course_facade.course_form()

    def localize_course(course):
        course_dct = course_form.fill_with_model(course)
        course_dct['edit_path'] = router.to_path(edit_path, course_dct['id'])
        course_dct['delete_path'] = router.to_path(delete_path, course_dct['id'])
        return course_dct

    localized_courses = [localize_course(course) for course in courses]
    context = {'courses': localized_courses,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'courses/course_home.html')

@login_not_required
@no_csrf
def delete(course_id):
    course_facade.delete_course_cmd(course_id)()
    return RedirectResponse(router.to_path(index))

