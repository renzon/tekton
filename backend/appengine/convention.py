import sys
from google.appengine.ext.webapp.blobstore_handlers import BlobstoreDownloadHandler, BlobstoreUploadHandler
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


class HandlerMixin():
    def get(self):
        self.make_convention()

    def post(self):
        self.make_convention()

    def make_convention(self):
        middleware.execute(settings.MIDDLEWARE_LIST, self)


class BaseHandler(HandlerMixin, webapp2.RequestHandler):
    pass


class DownloadHandler(HandlerMixin, BlobstoreDownloadHandler):
    pass


class UploadHandler(HandlerMixin, BlobstoreUploadHandler):
    pass


app = webapp2.WSGIApplication(
    [("/.*download.*", DownloadHandler), ("/.*upload.*", UploadHandler), ("/.*", BaseHandler)],
    debug=False)
