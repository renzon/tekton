# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
import tmpl
from web import my_form


class FormTests(unittest.TestCase):
    def test_index(self):
        # Mocking dependencies
        params = {}

        def write_tmpl_mock(template_name, values):
            params['template_name'] = template_name
            params['values'] = values
            tmpl.render(template_name, values)

        # fake http call
        my_form.index(write_tmpl_mock, 'Renzo')

        # Assertions
        self.assertEqual('templates/my_form.html', params.get('template_name'), 'Wrong template')
        self.assertDictEqual({'name': 'Renzo'}, params.get('values'), 'Wrong template values')


if __name__ == '__main__':
    unittest.main()
