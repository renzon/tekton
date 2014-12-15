# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import unittest
from google.appengine.api import files
from google.appengine.ext import testbed
import webapp2
from webapp2_extras import i18n
from config.template import render


# workaround for i18n. without this test will not run

app = webapp2.WSGIApplication(
    [webapp2.Route('/', None, name='upload_handler')])

request = webapp2.Request({'SERVER_NAME': 'test', 'SERVER_PORT': 80,
                           'wsgi.url_scheme': 'http'})
request.app = app
app.set_globals(app=app, request=request)

i18n.default_config['default_locale'] = 'en_US'
i18n.default_config['default_timezone'] = 'UTC'

# End of workaround

class GAETestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id="_")
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_mail_stub()
        self.testbed.init_taskqueue_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def assert_can_render(self, template_response):
        """
        Asserts that a template can be rendered. It raises an Exception otherwise
        :param template_response: a TemplateResponse instance
        :return:
        """
        render(template_response.template_path, template_response.context)

    def assert_can_serialize_as_json(self, json_response):
        """
        Asserts that a json_response contains json serializable data. It raises an Exception otherwise
        :param template_response: a JsonResponse or JsonUnsecureResponse instance
        :return:
        """
        json.dumps(json_response.context)


class BlobstoreTestCase(GAETestCase):
    def setUp(self):
        GAETestCase.setUp(self)
        self.testbed.init_blobstore_stub()
        self.testbed.init_files_stub()

    def save_blob(self, blobdata='blobdata'):
        file_name = files.blobstore.create(mime_type='application/octet-stream')
        with files.open(file_name, 'a') as f:
            f.write(blobdata)
        files.finalize(file_name)
        blob_key = files.blobstore.get_blob_key(file_name)
        return blob_key
