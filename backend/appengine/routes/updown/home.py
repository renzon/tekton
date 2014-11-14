# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext.blobstore import blobstore
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from tekton import router
from routes.updown import upload


@no_csrf
def index(_handler):
    """
    This is a example of file upload using
    Google Cloud Storage
    :return:
    """
    success_url = router.to_path(upload)
    bucket = get_default_gcs_bucket_name()
    logging.info(bucket)
    url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)
    context = {'upload_url': url}
    return TemplateResponse(context, 'up/home.html')