# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from course_app import facade
from web.courses import form


def delete(_handler, course_id):
    facade.delete_course_cmd(course_id)()
    _handler.redirect(router.to_path(index))


@no_csrf
def index():
    cmd = facade.list_courses_cmd()
    courses = cmd()
    form_edit_path = router.to_path(form.edit)
    delete_path = router.to_path(delete)

    def short_course_dict(course):
        course_dct = facade.short_course_dct(course)
        course_dct['edit_path'] = '/'.join([form_edit_path, course_dct['id']])
        course_dct['delete_path'] = '/'.join([delete_path, course_dct['id']])
        return course_dct

    short_courses = [short_course_dict(course) for course in courses]
    context = {'courses': short_courses,
               'course_form': router.to_path(form)}
    return TemplateResponse(context)

