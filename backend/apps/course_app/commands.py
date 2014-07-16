# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from course_app.model import Course

class CoursePublicForm(ModelForm):
    """
    Form used to show properties on app's home
    """
    _model_class = Course
    _include = [Course.d, 
                Course.f, 
                Course.i, 
                Course.price, 
                Course.start, 
                Course.name]


class CourseForm(ModelForm):
    """
    Form used to save and update operations on app's admin page
    """
    _model_class = Course
    _include = [Course.d, 
                Course.f, 
                Course.i, 
                Course.price, 
                Course.start, 
                Course.name]


class CourseDetailForm(ModelForm):
    """
    Form used to show entity details on app's admin page
    """
    _model_class = Course
    _include = [Course.d, 
                Course.f, 
                Course.i, 
                Course.price, 
                Course.creation, 
                Course.start, 
                Course.name]


class CourseShortForm(ModelForm):
    """
    Form used to show entity short version on app's admin page, mainly for tables
    """
    _model_class = Course
    _include = [Course.d, 
                Course.f, 
                Course.i, 
                Course.price, 
                Course.creation, 
                Course.start, 
                Course.name]


class SaveCourseCommand(SaveCommand):
    _model_form_class = CourseForm


class UpdateCourseCommand(UpdateNode):
    _model_form_class = CourseForm


class ListCourseCommand(ModelSearchCommand):
    def __init__(self):
        super(ListCourseCommand, self).__init__(Course.query_by_creation())

