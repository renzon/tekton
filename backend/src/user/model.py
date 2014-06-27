# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node


class N(Node):
    foo = ndb.StringProperty(required=True)
    blah = ndb.IntegerProperty(required=True)

