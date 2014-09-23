# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Course(Node):
    name = ndb.StringProperty(required=True)
    price = property.SimpleCurrency(required=True)
    start_date = ndb.DateProperty(required=True)

