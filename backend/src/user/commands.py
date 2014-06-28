# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from user.model import N


class NForm(ModelForm):
    _model_class = N
    _include = [N.blah, N.foo]


class NFormDetail(ModelForm):
    _model_class = N
    _include = [N.blah, N.foo, N.creation]

    def populate_form(self, model):
        dct = super(NFormDetail, self).populate_form(model)
        dct['id'] = unicode(model.key.id())
        return dct


class NFormShort(NFormDetail):
    _model_class = N
    _include = [N.foo]


class SaveNCommand(SaveCommand):
    _model_form_class = NForm


class UpdateNCommand(UpdateNode):
    _model_form_class = NForm


class ListNCommand(ModelSearchCommand):
    def __init__(self, page_size=100, start_cursor=None, offset=0, use_cache=True, cache_begin=True, **kwargs):
        super(ListNCommand, self).__init__(N.query_by_creation(), page_size, start_cursor, offset, use_cache,
                                           cache_begin, **kwargs)