# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Course(Node):
    name = ndb.StringProperty(required=True)
    price = property.SimpleCurrency(required=True)
    start = ndb.DateProperty(required=True)
    d = ndb.DateTimeProperty(required=True)
    i = ndb.IntegerProperty(required=True)
    d = property.SimpleDecimal(required=True)
    f = ndb.FloatProperty(required=True)

