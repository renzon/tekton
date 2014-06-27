# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tmpl_middleware import TemplateResponse
from web import my_form
from tekton import router


def index():
    url = router.to_path(my_form)
    return TemplateResponse({'form_url': url})
