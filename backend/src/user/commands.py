# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from user.model import User


class UserForm(ModelForm):
    _model_class = User
    _include = [User.age, User.name]


class UserFormDetail(ModelForm):
    _model_class = User
    _include = [User.age, User.name, User.creation]

    def populate_form(self, model):
        dct = super(UserFormDetail, self).populate_form(model)
        dct['id'] = unicode(model.key.id())
        return dct


class UserFormShort(UserFormDetail):
    _model_class = User
    _include = [User.name]


class SaveUserCommand(SaveCommand):
    _model_form_class = UserForm


class UpdateUserCommand(UpdateNode):
    _model_form_class = UserForm


class ListNCommand(ModelSearchCommand):
    def __init__(self, page_size=100, start_cursor=None, offset=0, use_cache=True, cache_begin=True, **kwargs):
        super(ListNCommand, self).__init__(User.query_by_creation(), page_size, start_cursor, offset, use_cache,
                                           cache_begin, **kwargs)