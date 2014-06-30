# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton.gae.middleware.json_middleware import JsonResponseMiddleware
from config.tmpl_middleware import TemplateMiddleware, TemplateWriteMiddleware
from tekton.gae.middleware.email_errors import EmailMiddleware
from tekton.gae.middleware.parameter import RequestParamsMiddleware
from tekton.gae.middleware.router_middleware import RouterMiddleware, ExecutionMiddleware
from tekton.gae.middleware.webapp2_dependencies import Webapp2Dependencies

SENDER_EMAIL = 'renzon@gmail.com'
WEB_BASE_PACKAGE = 'web'
DEFAULT_LOCALE = 'pt_BR'
DEFAULT_TIMEZONE = 'America/Sao_Paulo'
MIDDLEWARES = [TemplateMiddleware,
               EmailMiddleware,
               Webapp2Dependencies,
               RequestParamsMiddleware,
               RouterMiddleware,
               ExecutionMiddleware,
               TemplateWriteMiddleware,
               JsonResponseMiddleware]


