# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from user import facade


def index():
    cmd=facade.list_n()
    context = {'app': 'user'}
    return TemplateResponse(context)