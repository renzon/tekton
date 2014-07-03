# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.property import SimpleCurrency
from gaegraph.model import Node


class Course(Node):
    name = ndb.StringProperty(required=True)
    start_date = ndb.DateProperty(required=True)
    price = SimpleCurrency(required=True)

