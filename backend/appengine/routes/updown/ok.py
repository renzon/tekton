# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.updown import download
from tekton.router import to_path


@no_csrf
def index(blob_key):
    context = {'download_path': to_path(download, blob_key=blob_key)}
    return TemplateResponse(context, 'updown/ok.html')