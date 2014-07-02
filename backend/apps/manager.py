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


def save_%(model_underscore)s_cmd(**%(model_underscore)s_properties):
    """
    Command to save %(model)s entity
    :param %(model_underscore)s_properties: a dict of properties to save on model
    :return: a Command that save %(model)s, validating and localizing properties received as strings
    """
    return Save%(model)sCommand(**%(model_underscore)s_properties)


def update_%(model_underscore)s_cmd(%(model_underscore)s_id, **%(model_underscore)s_properties):
    """
    Command to update %(model)s entity with id equals '%(model_underscore)s_id'
    :param %(model_underscore)s_properties: a dict of properties to update model
    :return: a Command that update %(model)s, validating and localizing properties received as strings
    """
    return Update%(model)sCommand(%(model_underscore)s_id, **%(model_underscore)s_properties)


def list_%(model_underscore)ss_cmd():
    """
    Command to list %(model)s entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return List%(model)sCommand()


_detail_%(model_underscore)s_form = %(model)sFormDetail()


def detail_%(model_underscore)s_dct(%(model_underscore)s):
    """
    Function to localize %(model)s's detail properties.
    :param %(model_underscore)s: model %(model)s
    :return: dictionary with %(model)s's detail properties localized
    """
    return _detail_%(model_underscore)s_form.populate_form(%(model_underscore)s)


_short_%(model_underscore)s_form = %(model)sFormShort()


def short_%(model_underscore)s_dct(%(model_underscore)s):
    """
    Function to localize %(model)s's short properties. Common used to show data in tables.
    :param %(model_underscore)s: model %(model)s
    :return: dictionary with %(model)s's short properties localized
    """
    return _short_%(model_underscore)s_form.populate_form(%(model_underscore)s)


def get_%(model_underscore)s_cmd(%(model_underscore)s_id):
    """
    Find %(model_underscore)s by her id
    :param %(model_underscore)s_id: the %(model_underscore)s id
    :return: Command
    """
    return NodeSearch(%(model_underscore)s_id)


def delete_%(model_underscore)s_cmd(%(model_underscore)s_id):
    """
    Construct a command to delete a %(model)s
    :param %(model_underscore)s_id: %(model_underscore)s's id
    :return: Command
    """
    return DeleteNode(%(model_underscore)s_id)
'''

HOME_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from %(app_name)s import facade
from web.%(web_name)s import form


def delete(_handler, %(model_underscore)s_id):
    facade.delete_%(model_underscore)s_cmd(%(model_underscore)s_id)()
    _handler.redirect(router.to_path(index))


@no_csrf
def index():
    cmd = facade.list_%(model_underscore)ss_cmd()
    %(model_underscore)ss = cmd()
    form_edit_path = router.to_path(form.edit)
    delete_path = router.to_path(delete)

    def short_%(model_underscore)s_dict(%(model_underscore)s):
        %(model_underscore)s_dct = facade.short_%(model_underscore)s_dct(%(model_underscore)s)
        %(model_underscore)s_dct['edit_path'] = '/'.join([form_edit_path, %(model_underscore)s_dct['id']])
        %(model_underscore)s_dct['delete_path'] = '/'.join([delete_path, %(model_underscore)s_dct['id']])
        return %(model_underscore)s_dct

    short_%(model_underscore)ss = [short_%(model_underscore)s_dict(%(model_underscore)s) for %(model_underscore)s in %(model_underscore)ss]
    context = {'app': '%(model_underscore)s',
               '%(model_underscore)ss': short_%(model_underscore)ss,
               '%(model_underscore)s_form': router.to_path(form)}
    return TemplateResponse(context)
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


def _create_package(package_path):
    _create_dir_if_not_existing(package_path)
    _create_file_if_not_existing(os.path.join(package_path, '__init__.py'))


def _create_app(app_path, model):
    _create_package(app_path)
    _create_file_if_not_existing(os.path.join(app_path, 'model.py'),
                                 MODEL_TEMPLATE % {'model': model})


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


def _to_undescore_case(model):
    model_underscore=model[0].lower() + model[1:]
    return ''.join(('_' + letter.lower() if letter.isupper() else letter) for letter in model_underscore)


def facade_code_for(app, model):
    app_path = _to_app_name(app)
    model_underscore = _to_undescore_case(model)

    dct = {'app': app, 'app_path': app_path, 'model': model, 'model_underscore': model_underscore}
    return FACADE_TEMPLATE % dct


def _to_app_path(app):
    return os.path.join(APPS_DIR, app + '_app')


def init_facade(app, model):
    app_path = _to_app_path(app)
    facade_script = os.path.join(app_path, 'facade.py')
    content = facade_code_for(app, model)
    _create_file_if_not_existing(facade_script, content)
    return content


def _to_web_name(app):
    return app + 's'


def _to_web_path(app):
    return os.path.join(WEB_DIR, _to_web_name(app))


def init_web(app):
    web_path = _to_web_path(app)
    _create_package(web_path)


def code_for_home_script(app, model):
    web_name = _to_web_name(app)
    app_name = _to_app_name(app)
    return HOME_SCRIPT_TEMPLATE % {'app_name': app_name,
                                   'model_underscore': _to_undescore_case(model),
                                   'web_name':web_name}

def init_home_script(app, model):
    app_web_path = _to_web_path(app)
    home_script = os.path.join(app_web_path, 'home.py')
    content = code_for_home_script(app, model)
    _create_file_if_not_existing(home_script, content)
    return content



if __name__ == '__main__':
    # _title('Creating app package')
    # init_app('course', 'Course')
    #
    # _title('commands.py')
    # print init_commands('course', 'Course')
    # print init_facade('course', 'Course')
    # init_web('course')
    print init_home_script('course', 'Course')