import logging
import sys
import time
import os

# Put lib on path, once Google App Engine does not allow doing it directly
src_path = os.path.dirname(__file__)
src_path = os.path.join(src_path, '..')
src_path = os.path.normpath(src_path)
sys.path.append(os.path.join(src_path, 'lib'))
from gaepermission import facade

import webapp2


class BaseHandler(webapp2.RequestHandler):
    def get(self):
        # This import all paths so its good pre initialize them here
        init_time = time.time()
        facade.web_path_security_info()
        end_time = time.time()
        delta_seconds = (end_time - init_time)
        logging.info('Startup: %s miliseconds' % (delta_seconds*1000))



app = webapp2.WSGIApplication([('/.*', BaseHandler)], debug=False)

