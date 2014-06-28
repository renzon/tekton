# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import UpdateCommand
from user.commands import SaveNCommand, NForm, NFormDetail, UpdateNCommand, NFormShort, ListNCommand


def save_n(**n_properties):
    """
    Command to save N entity
    :param n_properties: a dict of properties to save on model
    :return: a Command that save N, validating and localizing properties received as strings
    """
    return SaveNCommand(**n_properties)


def update_n(n_id, **n_properties):
    """
    Command to update N entity with id equals 'n_id'
    :param n_properties: a dict of properties to update model
    :return: a Command that update N, validating and localizing properties received as strings
    """
    return UpdateNCommand(n_id, **n_properties)


def list_n():
    """
    Command to list N entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListNCommand()


_n_detail = NFormDetail()


def detail_n(n):
    """
    Function to localize N's detail properties
    :param n: model N
    :return: dictionary with N's detail properties localized
    """
    return _n_detail.populate_form(n)


_n_detail = NFormShort()


def short_n(n):
    """
    Function to localize N's detail properties
    :param n: model N
    :return: dictionary with N's detail properties localized
    """
    return _n_detail.populate_form(n)