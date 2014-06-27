# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from jinja2.exceptions import TemplateNotFound
from tekton import router
from tekton.gae.middleware.response import ResponseBase
import tmpl
from tekton.gae.middleware import Middleware


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
        self.dependencies["_render"] = tmpl.render


_TMPL_NOT_FOUND_MSG = '''Template not found
Looked by convention in /web/templates directory for:

1) %s
2) %s

Create one of the two template files or explicit indicate which one to use on TemplateResponse'''


class TemplateWriteMiddleware(Middleware):
    def set_up(self):
        fcn_response = self.dependencies['_fcn_response']
        fcn = self.dependencies['_fcn']
        if isinstance(fcn_response, TemplateResponse):
            context = fcn_response.context or {}
            template_path = fcn_response.template_path
            if template_path is None:
                template_path = router.to_path(fcn)

                def try_render(suffix):
                    if template_path == '/':
                        return '/home.html', tmpl.render('/home.html', context)

                    try:
                        template = template_path + suffix
                        return template, tmpl.render(template, context)
                    except TemplateNotFound:
                        return template, None

                template_1, tmpl_rendered = try_render('.html')
                if tmpl_rendered is None:
                    template_2, tmpl_rendered = try_render('/home.html')
                    if tmpl_rendered is None:
                        raise TemplateNotFound(_TMPL_NOT_FOUND_MSG % (template_1, template_2))


            else:
                tmpl_rendered = tmpl.render(template_path, context)
            self.handler.response.write(tmpl_rendered)
            return True  # after response, there is no need to look for more middlewares