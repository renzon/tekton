# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from user.commands import SaveUserCommand, UserFormDetail, UpdateUserCommand, UserFormShort, ListNCommand


def save_user(**user_properties):
    """
    Command to save User entity
    :param user_properties: a dict of properties to save on model
    :return: a Command that save User, validating and localizing properties received as strings
    """
    return SaveUserCommand(**user_properties)


def update_user(user_id, **user_properties):
    """
    Command to update User entity with id equals 'user_id'
    :param user_properties: a dict of properties to update model
    :return: a Command that update User, validating and localizing properties received as strings
    """
    return UpdateUserCommand(user_id, **user_properties)


def list_user():
    """
    Command to list User entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListNCommand()


_user_detail = UserFormDetail()


def detail_user(n):
    """
    Function to localize User's detail properties
    :param n: model User
    :return: dictionary with User's detail properties localized
    """
    return _user_detail.populate_form(n)


_user_detail = UserFormShort()


def short_user(n):
    """
    Function to localize User's detail properties
    :param n: model User
    :return: dictionary with User's detail properties localized
    """
    return _user_detail.populate_form(n)