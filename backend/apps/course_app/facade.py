# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from course_app.commands import ListCourseCommand, SaveCourseCommand, UpdateCourseCommand, \
    CoursePublicForm, CourseDetailForm, CourseShortForm


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


def course_detail_form(**kwargs):
    """
    Function to get Course's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return CourseDetailForm(**kwargs)


def course_short_form(**kwargs):
    """
    Function to get Course's short form. just a subset of course's properties
    :param kwargs: form properties
    :return: Form
    """
    return CourseShortForm(**kwargs)

def course_public_form(**kwargs):
    """
    Function to get Course'spublic form. just a subset of course's properties
    :param kwargs: form properties
    :return: Form
    """
    return CoursePublicForm(**kwargs)


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

