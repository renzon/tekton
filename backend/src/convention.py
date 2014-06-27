import sys
import os

#Put lib on path, once Google App Engine does not allow doing it directly
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import settings
from tekton.gae import middleware
import webapp2


class BaseHandler(webapp2.RequestHandler):
    def get(self):
        self.make_convention()

    def post(self):
        self.make_convention()

    def make_convention(self):
        middleware.execute(settings.MIDDLEWARES, self)


app = webapp2.WSGIApplication([("/.*", BaseHandler)], debug=False)

