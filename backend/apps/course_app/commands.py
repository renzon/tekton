# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from course_app.model import Course


class CourseForm(ModelForm):
    """
    Form used do save and update operations
    """
    _model_class = Course
    _include = [Course.price, 
                Course.start_date, 
                Course.name]


class CourseFormDetail(ModelForm):
    """
    Form used to show entity details
    """
    _model_class = Course
    _include = [Course.price, 
                Course.creation, 
                Course.start_date, 
                Course.name]

    def populate_form(self, model):
        dct = super(CourseFormDetail, self).populate_form(model)
        dct['id'] = unicode(model.key.id())
        return dct


class CourseFormShort(CourseFormDetail):
    """
    Form used to show entity short version, mainly for tables
    """
    _model_class = Course
    _include = [Course.price, 
                Course.creation, 
                Course.start_date, 
                Course.name]


class SaveCourseCommand(SaveCommand):
    _model_form_class = CourseForm


class UpdateCourseCommand(UpdateNode):
    _model_form_class = CourseForm


class ListCourseCommand(ModelSearchCommand):
    def __init__(self, page_size=100, start_cursor=None, offset=0, use_cache=True, cache_begin=True, **kwargs):
        super(ListCourseCommand, self).__init__(Course.query_by_creation(), page_size, start_cursor, offset, use_cache,
                                           cache_begin, **kwargs)

