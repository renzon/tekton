# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand
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


if __name__ == '__main__':
    print NFormDetail().populate_model()


class SaveNCommand(SaveCommand):
    _model_form_class = NForm


class UpdateNCommand(UpdateNode):
    _model_form_class = NForm
