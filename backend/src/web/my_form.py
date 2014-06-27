# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tmpl_middleware import TemplateResponse


def index(name):
    return TemplateResponse({'name': name})
