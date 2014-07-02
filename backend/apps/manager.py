# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import importlib
import os

# Templates

MODEL_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node


class %(model)s(Node):
    pass
'''

COMMANDS_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from %(app_path)s.model import %(model)s


class %(model)sForm(ModelForm):
    """
    Form used do save and update operations
    """
    _model_class = %(model)s
    _include = [%(form_properties)s]


class %(model)sFormDetail(ModelForm):
    """
    Form used to show entity details
    """
    _model_class = %(model)s
    _include = [%(full_properties)s]

    def populate_form(self, model):
        dct = super(%(model)sFormDetail, self).populate_form(model)
        dct['id'] = unicode(model.key.id())
        return dct


class %(model)sFormShort(%(model)sFormDetail):
    """
    Form used to show entity short version, mainly for tables
    """
    _model_class = %(model)s
    _include = [%(full_properties)s]


class Save%(model)sCommand(SaveCommand):
    _model_form_class = %(model)sForm


class Update%(model)sCommand(UpdateNode):
    _model_form_class = %(model)sForm


class List%(model)sCommand(ModelSearchCommand):
    def __init__(self, page_size=100, start_cursor=None, offset=0, use_cache=True, cache_begin=True, **kwargs):
        super(List%(model)sCommand, self).__init__(%(model)s.query_by_creation(), page_size, start_cursor, offset, use_cache,
                                           cache_begin, **kwargs)
'''

FACADE_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from %(app_path)s.commands import Save%(model)sCommand, %(model)sFormDetail, Update%(model)sCommand, %(model)sFormShort, List%(model)sCommand


def save_%(model_lower)s_cmd(**%(model_lower)s_properties):
    """
    Command to save %(model)s entity
    :param %(model_lower)s_properties: a dict of properties to save on model
    :return: a Command that save %(model)s, validating and localizing properties received as strings
    """
    return Save%(model)sCommand(**%(model_lower)s_properties)


def update_%(model_lower)s_cmd(%(model_lower)s_id, **%(model_lower)s_properties):
    """
    Command to update %(model)s entity with id equals '%(model_lower)s_id'
    :param %(model_lower)s_properties: a dict of properties to update model
    :return: a Command that update %(model)s, validating and localizing properties received as strings
    """
    return Update%(model)sCommand(%(model_lower)s_id, **%(model_lower)s_properties)


def list_%(model_lower)ss_cmd():
    """
    Command to list %(model)s entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return List%(model)sCommand()


_detail_%(model_lower)s_form = %(model)sFormDetail()


def detail_%(model_lower)s_dct(%(model_lower)s):
    """
    Function to localize %(model)s's detail properties.
    :param %(model_lower)s: model %(model)s
    :return: dictionary with %(model)s's detail properties localized
    """
    return _detail_%(model_lower)s_form.populate_form(%(model_lower)s)


_short_%(model_lower)s_form = %(model)sFormShort()


def short_%(model_lower)s_dct(%(model_lower)s):
    """
    Function to localize %(model)s's short properties. Common used to show data in tables.
    :param %(model_lower)s: model %(model)s
    :return: dictionary with %(model)s's short properties localized
    """
    return _short_%(model_lower)s_form.populate_form(%(model_lower)s)


def get_%(model_lower)s_cmd(%(model_lower)s_id):
    """
    Find %(model_lower)s by her id
    :param %(model_lower)s_id: the %(model_lower)s id
    :return: Command
    """
    return NodeSearch(%(model_lower)s_id)


def delete_%(model_lower)s_cmd(%(model_lower)s_id):
    """
    Construct a command to delete a %(model)s
    :param %(model_lower)s_id: %(model_lower)s's id
    :return: Command
    """
    return DeleteNode(%(model_lower)s_id)
'''

APPS_DIR = os.path.dirname(__file__)

PROJECT_DIR = os.path.join(APPS_DIR, '..')
WEB_DIR = os.path.join(PROJECT_DIR, 'plugins', 'appengine', 'web')


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


def _create_app(app_path, model):
    _create_package(app_path)
    _create_file_if_not_existing(os.path.join(app_path, 'model.py'),
                                 MODEL_TEMPLATE % {'model': model})


def _create_templates(name, web_path):
    name += 's'
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
    name += 's'
    handler_path = os.path.join(web_path, name)
    _create_package(handler_path)
    home_handler_path = os.path.join(handler_path, 'home.py')
    _create_file_if_not_existing(home_handler_path, content=HOME_HANDLER)


def init_app(name, model):
    app_path = os.path.join(APPS_DIR, name + '_app')
    _create_app(app_path, model)


PROPERTY = '%(model)s.%(property)s'


def _build_properties(model, properties):
    return ', \n                '.join([PROPERTY % {'model': model, 'property': p} for p in properties])


def commands_code_for(app, model):
    app_path = app + '_app'
    model_module = importlib.import_module(app_path + '.model')
    model_class = getattr(model_module, model)
    properties = set(model_class._properties.keys())
    properties = properties.difference(set(['class']))
    full_properties = _build_properties(model, properties)
    form_properties = properties.difference(set(['creation']))
    form_properties = _build_properties(model, form_properties)

    dct = {'app': app, 'app_path': app_path, 'model': model, 'full_properties': full_properties,
           'form_properties': form_properties}
    return COMMANDS_TEMPLATE % dct


def _title(param):
    n = 15
    print ('- ' * n) + param + (' -' * n)


def init_commands(app, model):
    app_path = os.path.join(APPS_DIR, app + '_app')
    commands_script = os.path.join(app_path, 'commands.py')
    content = commands_code_for(app, model)
    _create_file_if_not_existing(commands_script, content)
    return content


def _to_app_name(app):
    return app + '_app'


def facade_code_for(app, model):
    app_path = _to_app_name(app)
    model_lower = model[0].lower() + model[1:]
    model_lower = ''.join(('_' + letter.lower() if letter.isupper() else letter) for letter in model_lower)

    dct = {'app': app, 'app_path': app_path, 'model': model, 'model_lower': model_lower}
    return FACADE_TEMPLATE % dct


def _to_app_path(app):
    return os.path.join(APPS_DIR, app + '_app')


def init_facade(app, model):
    app_path = _to_app_path(app)
    facade_script = os.path.join(app_path, 'facade.py')
    content = facade_code_for(app, model)
    _create_file_if_not_existing(facade_script, content)
    return content


def _to_web_path(app):
    return os.path.join(WEB_DIR, app + 's')


def init_web(app):
    web_path = _to_web_path(app)
    _create_package(web_path)


def code_for_home_script(app, model):
    web_path = _to_web_path(app)
    app_name=_to_app_name(app)


if __name__ == '__main__':
    # _title('Creating app package')
    # init_app('course', 'Course')
    #
    # _title('commands.py')
    # print init_commands('course', 'Course')
    # print init_facade('course', 'Course')
    # init_web('course')
    print code_for_home_script('course','Course')