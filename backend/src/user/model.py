# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node


class User(Node):
    name = ndb.StringProperty(required=True)
    age = ndb.IntegerProperty(required=True)


