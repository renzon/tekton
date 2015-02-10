# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.middleware import CSRFMiddleware, CSRFInputToDependency
from locale_app.middleware import LocaleMiddleware
from multitenancy import MultitenacyMiddleware, set_subdomain, set_domain
from tekton.gae.middleware.json_middleware import JsonResponseMiddleware
from config.template_middleware import TemplateMiddleware, TemplateWriteMiddleware
from tekton.gae.middleware.email_errors import EmailMiddleware
from tekton.gae.middleware.parameter import RequestParamsMiddleware
from tekton.gae.middleware.redirect import RedirectMiddleware
from tekton.gae.middleware.router_middleware import RouterMiddleware, ExecutionMiddleware
from tekton.gae.middleware.webapp2_dependencies import Webapp2Dependencies
from gaepermission.middleware import LoggedUserMiddleware, PermissionMiddleware

APP_URL = 'https://tekton-fullstack.appspot.com'
SENDER_EMAIL = 'renzon@gmail.com'
DEFAULT_LOCALE = 'en_US'
DEFAULT_TIMEZONE = 'US/Eastern'
LOCALES = ['en_US', 'pt_BR']
TEMPLATE_404_ERROR = 'base/404.html'
TEMPLATE_400_ERROR = 'base/400.html'


MIDDLEWARE_LIST = [MultitenacyMiddleware,
                   LoggedUserMiddleware,
                   TemplateMiddleware,
                   EmailMiddleware,
                   Webapp2Dependencies,
                   RequestParamsMiddleware,
                   CSRFInputToDependency,
                   LocaleMiddleware,
                   RouterMiddleware,
                   CSRFMiddleware,
                   PermissionMiddleware,
                   ExecutionMiddleware,
                   TemplateWriteMiddleware,
                   JsonResponseMiddleware,
                   RedirectMiddleware]


