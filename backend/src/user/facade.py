# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from user.commands import SaveUserCommand, UserFormDetail, UpdateUserCommand, UserFormShort, ListUserCommand


def save_user_cmd(**user_properties):
    """
    Command to save User entity
    :param user_properties: a dict of properties to save on model
    :return: a Command that save User, validating and localizing properties received as strings
    """
    return SaveUserCommand(**user_properties)


def update_user_cmd(user_id, **user_properties):
    """
    Command to update User entity with id equals 'user_id'
    :param user_properties: a dict of properties to update model
    :return: a Command that update User, validating and localizing properties received as strings
    """
    return UpdateUserCommand(user_id, **user_properties)


def list_users_cmd():
    """
    Command to list User entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListUserCommand()


_detail_user_form = UserFormDetail()


def detail_user_dct(user):
    """
    Function to localize User's detail properties
    :param user: model User
    :return: dictionary with User's detail properties localized
    """
    return _detail_user_form.populate_form(user)


_short_user_form = UserFormShort()


def short_user_dct(user):
    """
    Function to localize User's detail properties
    :param user: model User
    :return: dictionary with User's short properties localized
    """
    return _short_user_form.populate_form(user)


def get_user_cmd(user_id):
    """
    Find user by her id
    :param user_id: the user id
    :return: Command
    """
    return NodeSearch(user_id)


def delete_user_cmd(user_id):
    """
    Construct a command to delete a User
    :param user_id: user's id
    :return: Command
    """
    return DeleteNode(user_id)
