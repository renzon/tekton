# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from collections import defaultdict
from unittest.case import TestCase
from multitenancy import get_namespace
import multitenancy


class GetNamespaceTests(TestCase):
    def setUp(self):
        multitenancy._subdomain_dct = defaultdict(lambda: '')
        multitenancy._domain_dct = {}

    def test_not_registered_namespace(self):
        self.assertEqual('', get_namespace('www'))
        self.assertEqual('', get_namespace('www.foo.bar'))

    def test_registered_domain(self):
        multitenancy.set_domain('www.foo.bar', 'some_namespace')
        self.assertEqual('', get_namespace('www'))
        self.assertEqual('some_namespace', get_namespace('www.foo.bar'))

    def test_registered_subdomain(self):
        multitenancy.set_subdomain('www', 'some_namespace')
        self.assertEqual('some_namespace', get_namespace('www'))
        self.assertEqual('some_namespace', get_namespace('www.foo.bar'))

    def test_domain_precedence(self):
        multitenancy.set_domain('www.foo.bar', 'some_namespace')
        multitenancy.set_subdomain('www', 'other_namespace')
        self.assertEqual('other_namespace', get_namespace('www'))
        self.assertEqual('some_namespace', get_namespace('www.foo.bar'))
        self.assertEqual('other_namespace', get_namespace('www.anotherdomain'))

    def test_domain_with_port(self):
        multitenancy.set_domain('www.foo.bar', 'some_namespace')
        multitenancy.set_subdomain('www', 'other_namespace')
        self.assertEqual('other_namespace', get_namespace('www'))
        self.assertEqual('some_namespace', get_namespace('www.foo.bar:8080'))
