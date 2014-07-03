# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from course_app.commands import SaveCourseCommand, CourseFormDetail, UpdateCourseCommand, CourseFormShort, ListCourseCommand


def save_course_cmd(**course_properties):
    """
    Command to save Course entity
    :param course_properties: a dict of properties to save on model
    :return: a Command that save Course, validating and localizing properties received as strings
    """
    return SaveCourseCommand(**course_properties)


def update_course_cmd(course_id, **course_properties):
    """
    Command to update Course entity with id equals 'course_id'
    :param course_properties: a dict of properties to update model
    :return: a Command that update Course, validating and localizing properties received as strings
    """
    return UpdateCourseCommand(course_id, **course_properties)


def list_courses_cmd():
    """
    Command to list Course entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListCourseCommand()


_detail_course_form = CourseFormDetail()


def detail_course_dct(course):
    """
    Function to localize Course's detail properties.
    :param course: model Course
    :return: dictionary with Course's detail properties localized
    """
    return _detail_course_form.populate_form(course)


_short_course_form = CourseFormShort()


def short_course_dct(course):
    """
    Function to localize Course's short properties. Common used to show data in tables.
    :param course: model Course
    :return: dictionary with Course's short properties localized
    """
    return _short_course_form.populate_form(course)


def get_course_cmd(course_id):
    """
    Find course by her id
    :param course_id: the course id
    :return: Command
    """
    return NodeSearch(course_id)


def delete_course_cmd(course_id):
    """
    Construct a command to delete a Course
    :param course_id: course's id
    :return: Command
    """
    return DeleteNode(course_id)

