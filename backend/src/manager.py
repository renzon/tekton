# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

SRC_DIR = os.path.dirname(__file__)


def _create_dir_if_not_existing(package_path):
    if not os.path.exists(package_path):
        os.mkdir(package_path)


def _create_file_if_not_existing(file_path, content=''):
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            f.write(content.encode('utf8'))


PY_HEADER = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals'''

HOME_HTML = '''<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <h1>This is the automatic generated page for App "%s"</h1>
</body>
</html>'''


def _create_package(package_path):
    _create_dir_if_not_existing(package_path)
    _create_file_if_not_existing(os.path.join(package_path, '__init__.py'))


def _create_app(app_path):
    _create_package(app_path)
    _create_file_if_not_existing(os.path.join(app_path, 'model.py'), PY_HEADER)
    _create_file_if_not_existing(os.path.join(app_path, 'commands.py'), PY_HEADER)
    _create_file_if_not_existing(os.path.join(app_path, 'facade.py'), PY_HEADER)


def _create_templates(name, web_path):
    templates_path = os.path.join(web_path, 'templates')
    _create_dir_if_not_existing(templates_path)
    templates_path = os.path.join(templates_path, name)
    _create_dir_if_not_existing(templates_path)
    home_file = os.path.join(templates_path, 'home.html')
    _create_file_if_not_existing(home_file, HOME_HTML % name)


HOME_HANDLER = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse


def index():
    return TemplateResponse()'''


def _create_app_handler(web_path, name):
    handler_path = os.path.join(web_path, name)
    _create_package(handler_path)
    home_handler_path = os.path.join(handler_path, 'home.py')
    _create_file_if_not_existing(home_handler_path, content=HOME_HANDLER)


def create_app(name):
    app_path = os.path.join(SRC_DIR, name)
    _create_app(app_path)
    web_path = os.path.join(SRC_DIR, 'web')
    _create_app_handler(web_path, name)
    _create_package(web_path)
    _create_templates(name, web_path)


if __name__ == '__main__':
    print create_app('user')