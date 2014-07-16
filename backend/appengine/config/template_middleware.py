# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from jinja2.exceptions import TemplateNotFound
from tekton import router
from tekton.gae.middleware.response import ResponseBase
from tekton.gae.middleware import Middleware

from config import template


class TemplateResponse(ResponseBase):
    def __init__(self, context=None, template_path=None):
        """
        Class to render template and send it through HTTP response
        context: the context dict form template rendering
        template_path: the path for te template. If None it will find the template by convention, according to path
        """

        super(TemplateResponse, self).__init__(context)
        self.template_path = template_path


class TemplateMiddleware(Middleware):
    def set_up(self):
        self.dependencies["_render"] = template.render


_TMPL_NOT_FOUND_MSG = '''Template not found
Looked by convention in /routes/templates directory for:

1) %s
2) %s

Create one of the two template files or explicit indicate which one to use on TemplateResponse'''


def render_by_convention(fcn, context):
    template_path = router.to_path(fcn)

    def try_render(suffix):
        if template_path == '/':
            return '/home.html', template.render('/home.html', context)

        try:
            template_file = template_path + suffix
            return template_file, template.render(template_file, context)
        except TemplateNotFound:
            return template_file, None

    template_1, tmpl_rendered = try_render('.html')
    if tmpl_rendered is None:
        template_2, tmpl_rendered = try_render('/home.html')
        if tmpl_rendered is None:
            raise TemplateNotFound(_TMPL_NOT_FOUND_MSG % (template_1, template_2))
    return tmpl_rendered


class TemplateWriteMiddleware(Middleware):
    def set_up(self):
        fcn_response = self.dependencies['_fcn_response']
        fcn = self.dependencies['_fcn']
        if isinstance(fcn_response, TemplateResponse):
            context = fcn_response.context or {}
            for key in ('_logged_user', '_login_path', '_logout_path'):
                context[key] = self.dependencies[key]
            if '_csrf_code' in self.dependencies:
                context['_csrf_code'] = self.dependencies['_csrf_code']
            template_path = fcn_response.template_path
            if template_path is None:
                tmpl_rendered = render_by_convention(fcn, context)


            else:
                tmpl_rendered = template.render(template_path, context)
            self.handler.response.write(tmpl_rendered)
            return True  # after response, there is no need to look for more middlewares