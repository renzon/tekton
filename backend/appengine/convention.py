import sys
import os

# Put lib on path, once Google App Engine does not allow doing it directly
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
sys.path.append(os.path.join(os.path.dirname(__file__), "apps"))

import settings
from tekton.gae import middleware
import webapp2
from webapp2_extras import i18n

i18n.default_config['default_locale'] = settings.DEFAULT_LOCALE
i18n.default_config['default_timezone'] = settings.DEFAULT_TIMEZONE


class BaseHandler(webapp2.RequestHandler):
    def get(self):
        self.make_convention()

    def post(self):
        self.make_convention()

    def make_convention(self):
        middleware.execute(settings.MIDDLEWARE_LIST, self)


app = webapp2.WSGIApplication([("/.*", BaseHandler)], debug=False)

