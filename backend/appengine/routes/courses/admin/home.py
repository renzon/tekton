# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from course_app import facade
from routes.courses.admin import new, edit


def delete(_handler, course_id):
    facade.delete_course_cmd(course_id)()
    _handler.redirect(router.to_path(index))


@no_csrf
def index():
    cmd = facade.list_courses_cmd()
    courses = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    short_form = facade.course_short_form()

    def short_course_dict(course):
        course_dct = short_form.fill_with_model(course)
        course_dct['edit_path'] = router.to_path(edit_path, course_dct['id'])
        course_dct['delete_path'] = router.to_path(delete_path, course_dct['id'])
        return course_dct

    short_courses = [short_course_dict(course) for course in courses]
    context = {'courses': short_courses,
               'new_path': router.to_path(new)}
    return TemplateResponse(context)

