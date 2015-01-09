# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import importlib
import sys
import os
import shutil

if 'GAE_SDK' in os.environ:
    SDK_PATH = os.environ['GAE_SDK']

    sys.path.insert(0, SDK_PATH)

    import dev_appserver

    dev_appserver.fix_sys_path()
else:
    print "GAE_SDK environment variable must be on path and point to App Engine's SDK folder"
from gaeforms.ndb.property import SimpleCurrency, SimpleDecimal
from google.appengine.ext.ndb.model import StringProperty, TextProperty, DateProperty, DateTimeProperty, \
    IntegerProperty, \
    FloatProperty, BooleanProperty

PROJECT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))
APPS_DIR = os.path.join(PROJECT_DIR, 'apps')
TEST_DIR = os.path.join(PROJECT_DIR, 'test')
sys.path.insert(1, APPS_DIR)
APPENGINE_DIR = os.path.join(PROJECT_DIR, 'appengine')
WEB_DIR = os.path.join(APPENGINE_DIR, 'routes')
TEMPLATES_DIR = os.path.join(APPENGINE_DIR, 'templates')
# Templates

REST_TESTS_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from %(app)s_app.%(app)s_model import %(model)s
from routes.%(app)ss import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(%(model)s)
        mommy.save_one(%(model)s)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        %(model_underscore)s_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', %(model_properties)s]), set(%(model_underscore)s_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(%(model)s.query().get())
        json_response = rest.new(None, %(request_values)s)
        db_%(model_underscore)s = %(model)s.query().get()
        self.assertIsNotNone(db_%(model_underscore)s)
%(model_assertions)s
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set([%(model_properties)s]), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        %(model_underscore)s = mommy.save_one(%(model)s)
        old_properties = %(model_underscore)s.to_dict()
        json_response = rest.edit(None, %(model_underscore)s.key.id(), %(request_values)s)
        db_%(model_underscore)s = %(model_underscore)s.key.get()
%(model_assertions)s
        self.assertNotEqual(old_properties, db_%(model_underscore)s.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        %(model_underscore)s = mommy.save_one(%(model)s)
        old_properties = %(model_underscore)s.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, %(model_underscore)s.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set([%(model_properties)s]), set(errors.keys()))
        self.assertEqual(old_properties, %(model_underscore)s.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        %(model_underscore)s = mommy.save_one(%(model)s)
        rest.delete(None, %(model_underscore)s.key.id())
        self.assertIsNone(%(model_underscore)s.key.get())

    def test_non_%(model_underscore)s_deletion(self):
        non_%(model_underscore)s = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_%(model_underscore)s.key.id())
        self.assertIsNotNone(non_%(model_underscore)s.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

'''

HOME_TESTS_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from %(app)s_app.%(app)s_model import %(model)s
from routes.%(app)ss.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(%(model)s)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        %(model_underscore)s = mommy.save_one(%(model)s)
        redirect_response = delete(%(model_underscore)s.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(%(model_underscore)s.key.get())

    def test_non_%(model_underscore)s_deletion(self):
        non_%(model_underscore)s = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_%(model_underscore)s.key.id())
        self.assertIsNotNone(non_%(model_underscore)s.key.get())

'''

EDIT_TESTS_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from %(app)s_app.%(app)s_model import %(model)s
from routes.%(app)ss.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        %(model_underscore)s = mommy.save_one(%(model)s)
        template_response = index(%(model_underscore)s.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        %(model_underscore)s = mommy.save_one(%(model)s)
        old_properties = %(model_underscore)s.to_dict()
        redirect_response = save(%(model_underscore)s.key.id(), %(request_values)s)
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_%(model_underscore)s = %(model_underscore)s.key.get()
%(model_assertions)s
        self.assertNotEqual(old_properties, edited_%(model_underscore)s.to_dict())

    def test_error(self):
        %(model_underscore)s = mommy.save_one(%(model)s)
        old_properties = %(model_underscore)s.to_dict()
        template_response = save(%(model_underscore)s.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set([%(model_properties)s]), set(errors.keys()))
        self.assertEqual(old_properties, %(model_underscore)s.key.get().to_dict())
        self.assert_can_render(template_response)
'''

NEW_TESTS_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from %(app)s_app.%(app)s_model import %(model)s
from routes.%(app)ss.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(%(model)s.query().get())
        redirect_response = save(%(request_values)s)
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_%(model_underscore)s = %(model)s.query().get()
        self.assertIsNotNone(saved_%(model_underscore)s)
%(model_assertions)s

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set([%(model_properties)s]), set(errors.keys()))
        self.assert_can_render(template_response)
'''

MODEL_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class %(model)s(Node):
%(properties)s

'''

COMMANDS_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from %(app_path)s.%(app)s_model import %(model)s



class %(model)sSaveForm(ModelForm):
    """
    Form used to save and update %(model)s
    """
    _model_class = %(model)s
    _include = [%(form_properties)s]


class %(model)sForm(ModelForm):
    """
    Form used to expose %(model)s's properties for list or json
    """
    _model_class = %(model)s


class Get%(model)sCommand(NodeSearch):
    _model_class = %(model)s


class Delete%(model)sCommand(DeleteNode):
    _model_class = %(model)s


class Save%(model)sCommand(SaveCommand):
    _model_form_class = %(model)sSaveForm


class Update%(model)sCommand(UpdateNode):
    _model_form_class = %(model)sSaveForm


class List%(model)sCommand(ModelSearchCommand):
    def __init__(self):
        super(List%(model)sCommand, self).__init__(%(model)s.query_by_creation())

'''

FACADE_TEMPLATE = r'''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from %(app_path)s.%(app)s_commands import List%(model)sCommand, Save%(model)sCommand, Update%(model)sCommand, %(model)sForm,\
    Get%(model)sCommand, Delete%(model)sCommand


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


def %(model_underscore)s_form(**kwargs):
    """
    Function to get %(model)s's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return %(model)sForm(**kwargs)


def get_%(model_underscore)s_cmd(%(model_underscore)s_id):
    """
    Find %(model_underscore)s by her id
    :param %(model_underscore)s_id: the %(model_underscore)s id
    :return: Command
    """
    return Get%(model)sCommand(%(model_underscore)s_id)



def delete_%(model_underscore)s_cmd(%(model_underscore)s_id):
    """
    Construct a command to delete a %(model)s
    :param %(model_underscore)s_id: %(model_underscore)s's id
    :return: Command
    """
    return Delete%(model)sCommand(%(model_underscore)s_id)

'''
HOME_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from %(app_name)s import %(app)s_facade
from routes.%(web_name)s import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = %(app)s_facade.list_%(model_underscore)ss_cmd()
    %(model_underscore)ss = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    %(model_underscore)s_form = %(app)s_facade.%(model_underscore)s_form()

    def localize_%(model_underscore)s(%(model_underscore)s):
        %(model_underscore)s_dct = %(model_underscore)s_form.fill_with_model(%(model_underscore)s)
        %(model_underscore)s_dct['edit_path'] = router.to_path(edit_path, %(model_underscore)s_dct['id'])
        %(model_underscore)s_dct['delete_path'] = router.to_path(delete_path, %(model_underscore)s_dct['id'])
        return %(model_underscore)s_dct

    localized_%(model_underscore)ss = [localize_%(model_underscore)s(%(model_underscore)s) for %(model_underscore)s in %(model_underscore)ss]
    context = {'%(model_underscore)ss': localized_%(model_underscore)ss,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, '%(app)ss/%(app)s_home.html')


def delete(%(model_underscore)s_id):
    %(app)s_facade.delete_%(model_underscore)s_cmd(%(model_underscore)s_id)()
    return RedirectResponse(router.to_path(index))

'''

NEW_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from %(app_name)s import %(app)s_facade
from routes import %(web_name)s
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, '%(web_name)s/%(app)s_form.html')


def save(**%(model_underscore)s_properties):
    cmd = %(app)s_facade.save_%(model_underscore)s_cmd(**%(model_underscore)s_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   '%(model_underscore)s': %(model_underscore)s_properties}

        return TemplateResponse(context, '%(web_name)s/%(app)s_form.html')
    return RedirectResponse(router.to_path(%(web_name)s))

'''

EDIT_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from %(app_name)s import %(app)s_facade
from routes import %(web_name)s
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(%(model_underscore)s_id):
    %(model_underscore)s = %(app)s_facade.get_%(model_underscore)s_cmd(%(model_underscore)s_id)()
    %(model_underscore)s_form = %(app)s_facade.%(model_underscore)s_form()
    context = {'save_path': router.to_path(save, %(model_underscore)s_id), '%(model_underscore)s': %(model_underscore)s_form.fill_with_model(%(model_underscore)s)}
    return TemplateResponse(context, '%(web_name)s/%(app)s_form.html')


def save(%(model_underscore)s_id, **%(model_underscore)s_properties):
    cmd = %(app)s_facade.update_%(model_underscore)s_cmd(%(model_underscore)s_id, **%(model_underscore)s_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, '%(model_underscore)s': %(model_underscore)s_properties}

        return TemplateResponse(context, '%(web_name)s/%(app)s_form.html')
    return RedirectResponse(router.to_path(%(web_name)s))

'''

REST_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from %(app_name)s import %(app)s_facade


def index():
    cmd = %(app)s_facade.list_%(model_underscore)ss_cmd()
    %(model_underscore)s_list = cmd()
    %(model_underscore)s_form = %(app)s_facade.%(model_underscore)s_form()
    %(model_underscore)s_dcts = [%(model_underscore)s_form.fill_with_model(m) for m in %(model_underscore)s_list]
    return JsonResponse(%(model_underscore)s_dcts)


def new(_resp, **%(model_underscore)s_properties):
    cmd = %(app)s_facade.save_%(model_underscore)s_cmd(**%(model_underscore)s_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **%(model_underscore)s_properties):
    cmd = %(app)s_facade.update_%(model_underscore)s_cmd(id, **%(model_underscore)s_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = %(app)s_facade.delete_%(model_underscore)s_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        %(model_underscore)s = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    %(model_underscore)s_form = %(app)s_facade.%(model_underscore)s_form()
    return JsonResponse(%(model_underscore)s_form.fill_with_model(%(model_underscore)s))

'''

HOME_HTML_TEMPLATE = '''{%% extends '%(web_name)s/%(app)s_base.html' %%}
{%% block body %%}
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h1>{%% trans %%}This is a generic home for %(app_name)s {%% endtrans %%}  </h1>
                <a href="{{ new_path }}" class="btn btn-success">{%% trans %%}Create New %(model)s{%% endtrans %%}</a>
                <hr/>
                <h2>{%% trans %%}List of %(model)ss{%% endtrans %%}</h2>
                <table class="table table-striped table-hover">
                    <thead>
                    <tr>
                        <th/>
                        <th>{%% trans %%}Id{%% endtrans %%}</th>
                        <th>{%% trans %%}Creation{%% endtrans %%}</th>
%(headers)s
                    </tr>
                    </thead>
                    <tbody>
                    {%% for %(model_underscore)s in %(model_underscore)ss %%}
                        <tr>
                            <td><a href="{{ %(model_underscore)s.edit_path }}" class="btn btn-success btn-sm"><i
                                    class="glyphicon glyphicon-pencil"></i></a></td>
                            <td>{{ %(model_underscore)s.id }}</td>
                            <td>{{ %(model_underscore)s.creation }}</td>
%(columns)s
                            <td>
                                <form action="{{ %(model_underscore)s.delete_path }}" method="post" onsubmit="return confirm('{{_('Are you sure to delete? Press cancel to avoid deletion.')}}');">
                                    {{ csrf_input() }}
                                    <button class="btn btn-danger btn-sm"><i
                                            class="glyphicon glyphicon-trash"></i></button>
                                </form>
                            </td>
                        </tr>
                    {%% endfor %%}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
{%% endblock %%}'''

FORM_HTML_TEMPLATE = '''{%% extends '%(web_name)s/%(app)s_base.html' %%}
{%% block body %%}
    {%% set %(model_underscore)s=%(model_underscore)s or None %%}
    {%% set errors=errors or None %%}
    <div class="container">
        <div class="row">
            <div class="col-md-6 col-md-offset-3">
                <br/>

                <div class="well">
                    <h1 class="text-center">{%% trans %%}%(model)s Form{%% endtrans %%}</h1>

                    <form action="{{ save_path }}" method="post" role="form">
                        {{ csrf_input() }}
%(inputs)s
                        <button type="submit" class="btn btn-success">{%% trans %%}Save{%% endtrans %%}</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

{%% endblock %%}'''


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


def _create_app(name, app_path, model, *properties):
    properties = '\n'.join(parse_property(p) for p in properties)
    properties = properties or '    pass'
    _create_package(app_path)
    _create_file_if_not_existing(os.path.join(app_path, '%s_model.py' % name),
                                 MODEL_TEMPLATE % {'model': model, 'properties': properties})


def parse_property(p):
    name, type_alias = p.split(':')
    types = {'string': 'ndb.StringProperty(required=True)',
             'date': 'ndb.DateProperty(required=True)',
             'datetime': 'ndb.DateTimeProperty(required=True)',
             'int': 'ndb.IntegerProperty(required=True)',
             'float': 'ndb.FloatProperty(required=True)',
             'decimal': 'property.SimpleDecimal(required=True)',
             'currency': 'property.SimpleCurrency(required=True)',
             'bool': 'ndb.BooleanProperty(required=True)'}
    return '    %s = %s' % (name, types[type_alias])


def init_app(name, model, *properties):
    _title('Creating app package')
    app_path = os.path.join(APPS_DIR, name + '_app')
    _create_app(name, app_path, model, *properties)


PROPERTY = '%(model)s.%(property)s'


def _build_properties(model, properties):
    return ', \n                '.join([PROPERTY % {'model': model, 'property': p} for p in properties])


def _model_class(app, model):
    app_path = app + '_app'
    model_module = importlib.import_module(app_path + '.%s_model' % app)
    model_class = getattr(model_module, model)
    return model_class


def _model_properties(app, model):
    model_class = _model_class(app, model)
    properties = set(model_class._properties.keys())
    properties = properties.difference(set(['class']))
    return properties


def commands_code_for(app, model):
    app_path = app + '_app'
    properties = _model_properties(app, model)
    full_properties = _build_properties(model, properties)
    form_properties = properties.difference(set(['creation']))
    form_properties = _build_properties(model, form_properties)

    dct = {'app': app, 'app_path': app_path, 'model': model, 'full_properties': full_properties,
           'form_properties': form_properties}
    return COMMANDS_TEMPLATE % dct


def _title(param):
    n = 15
    print ('- ' * n) + param + (' -' * n)


def _to_app_name(app):
    return app + '_app'


def _to_underscore_case(model):
    model_underscore = model[0].lower() + model[1:]
    return ''.join(('_' + letter.lower() if letter.isupper() else letter) for letter in model_underscore)


def generate_generic(app, model, template_path_function, file_name, content_function):
    app_template_path = template_path_function(app)
    template_file = os.path.join(app_template_path, file_name)
    content = content_function(app, model)
    _create_file_if_not_existing(template_file, content)
    return content


def _to_app_path(app):
    return os.path.join(APPS_DIR, app + '_app')


def generate_app_file(app, model, file_name, content_function):
    file_name = '%s_%s.py' % (app, file_name)
    return generate_generic(app, model, _to_app_path, file_name, content_function)


def init_commands(app, model):
    return generate_app_file(app, model, 'commands', commands_code_for)


def facade_code_for(app, model):
    app_path = _to_app_name(app)
    model_underscore = _to_underscore_case(model)

    dct = {'app': app, 'app_path': app_path, 'model': model, 'model_underscore': model_underscore}
    return FACADE_TEMPLATE % dct


def init_facade(app, model):
    return generate_app_file(app, model, 'facade', facade_code_for)


def _to_routes_name(app):
    return app + 's'


def init_routes(app):
    web_path = _to_routes_path(app)
    _create_package(web_path)


def _to_routes_path(app):
    return os.path.join(WEB_DIR, _to_routes_name(app))


def generate_routes(app, model, file_name, content_function):
    file_name = '%s.py' % file_name
    return generate_generic(app, model, _to_routes_path, file_name, content_function)


def code_for_home_script(app, model):
    web_name = _to_routes_name(app)
    app_name = _to_app_name(app)
    return HOME_SCRIPT_TEMPLATE % {'app_name': app_name,
                                   'model_underscore': _to_underscore_case(model),
                                   'web_name': web_name,
                                   'app': app}


def init_home_script(app, model):
    return generate_routes(app, model, 'home', code_for_home_script)


def code_for_new_script(app, model):
    web_name = _to_routes_name(app)
    app_name = _to_app_name(app)
    return NEW_SCRIPT_TEMPLATE % {'app_name': app_name,
                                  'model_underscore': _to_underscore_case(model),
                                  'web_name': web_name,
                                  'app': app}


def init_new_script(app, model):
    return generate_routes(app, model, 'new', code_for_new_script)


def code_for_edit_script(app, model):
    web_name = _to_routes_name(app)
    app_name = _to_app_name(app)
    return EDIT_SCRIPT_TEMPLATE % {'app_name': app_name,
                                   'model_underscore': _to_underscore_case(model),
                                   'web_name': web_name,
                                   'app': app}


def init_edit_script(app, model):
    return generate_routes(app, model, 'edit', code_for_edit_script)


def code_for_rest_script(app, model):
    web_name = _to_routes_name(app)
    app_name = _to_app_name(app)
    return REST_SCRIPT_TEMPLATE % {'app_name': app_name,
                                   'model_underscore': _to_underscore_case(model),
                                   'web_name': web_name,
                                   'app': app}


def init_rest_script(app, model):
    return generate_routes(app, model, 'rest', code_for_rest_script)


APP_BASE_HTML_TEMPLATE = '''{%% extends 'base/base.html' %%}
{%% block tabs %%}
    {{ select_tab('%(app_name_upper)s') }}
{%% endblock %%}'''


def _to_template_path(app):
    return os.path.join(TEMPLATES_DIR, _to_routes_name(app))


def init_html_templates(app):
    template_path = _to_template_path(app)
    content = APP_BASE_HTML_TEMPLATE % {'app_name_upper': _to_routes_name(app).upper()}
    _create_dir_if_not_existing(template_path)
    base_dir = os.path.join(template_path, '%s_base.html' % app)
    _create_file_if_not_existing(base_dir, content)


def _to_label(label):
    names = label.split('_')
    upper_names = [n[0].upper() + n[1:] for n in names]
    return ' '.join(upper_names)


def _to_html_table_header(properties):
    template = ' ' * 24 + '<th>{%% trans %%}%s{%% endtrans %%}</th>'
    properties = [_to_label(p) for p in properties]
    rendered = [template % p for p in properties]
    return '\n'.join(rendered)


def _to_html_table_columns(model_underscore, properties):
    template = ' ' * 28 + '<td>{{ %(model_underscore)s.%(property)s }}</td>'

    rendered = [template % {'model_underscore': model_underscore, 'property': p} for p in properties]
    return '\n'.join(rendered)


def _to_html_form_inputs(model_underscore, properties):
    template = "{{ form_input(_('%(label)s'),'%(property)s',%(model_underscore)s.%(property)s,errors.%(property)s) }}"
    template = ' ' * 24 + template

    rendered = [template % {'model_underscore': model_underscore, 'property': p, 'label': _to_label(p)} for p in
                properties]
    return '\n'.join(rendered)


def generate_template(app, model, file_name, content_function):
    file_name = '%s_%s.html' % (app, file_name)
    return generate_generic(app, model, _to_template_path, file_name, content_function)


def code_for_home_html(app, model):
    web_name = _to_routes_name(app)
    app_name = _to_app_name(app)
    properties = _model_properties(app, model)
    properties = properties.difference(set(['creation']))
    model_underscore = _to_underscore_case(model)
    return HOME_HTML_TEMPLATE % {'app_name': app_name,
                                 'model_underscore': model_underscore,
                                 'model': model,
                                 'web_name': web_name,
                                 'headers': _to_html_table_header(properties),
                                 'columns': _to_html_table_columns(model_underscore, properties),
                                 'app': app}


def init_home_html(app, model):
    return generate_template(app, model, 'home', code_for_home_html)


def code_for_form_html(app, model):
    web_name = _to_routes_name(app)
    app_name = _to_app_name(app)
    properties = _model_properties(app, model)
    properties = properties.difference(set(['creation']))
    model_underscore = _to_underscore_case(model)
    return FORM_HTML_TEMPLATE % {'app_name': app_name,
                                 'model_underscore': model_underscore,
                                 'model': model,
                                 'web_name': web_name,
                                 'inputs': _to_html_form_inputs(model_underscore, properties),
                                 'app': app}


def init_form_html(app, model):
    return generate_template(app, model, 'form', code_for_form_html)


def init_test(name, model, *properties):
    _title('Creating test package')
    test_path = os.path.join(TEST_DIR, name + '_tests')
    _create_package(test_path)


def _to_test_path(app):
    return os.path.join(TEST_DIR, app + '_tests')


def generate_tests(app, model, file_name, content_function):
    file_name = '%s_%s_tests.py' % (app, file_name)
    return generate_generic(app, model, _to_test_path, file_name, content_function)


def _to_default_model_value(descriptor, name, index):
    if isinstance(descriptor, (StringProperty, TextProperty)):
        return "'%s_string'" % name
    if isinstance(descriptor, DateProperty):
        return "date(2014, 1, %s)" % (index + 1)
    if isinstance(descriptor, DateTimeProperty):
        return "datetime(2014, 1, 1, 1, %s, 0)" % (index + 1)
    if isinstance(descriptor, (SimpleCurrency, SimpleDecimal)):
        return "Decimal('1.%s')" % (index + 1 if index >= 9 else '0%s' % (index + 1))
    if isinstance(descriptor, IntegerProperty):
        return "%s" % (index + 1)
    if isinstance(descriptor, FloatProperty):
        return "1.%s" % (index + 1)
    if isinstance(descriptor, BooleanProperty):
        return "True"


def _to_model_assertions(variable, descriptors_dct):
    template = "        self.assertEquals(%(value)s, %(variable)s.%(property)s)"
    rendered = [template % {'variable': variable, 'property': p, 'value': _to_default_model_value(descriptor, p, i)} for
                i, (p, descriptor) in
                enumerate(descriptors_dct.iteritems())]
    return '\n'.join(rendered)


def _to_default_reques_value(descriptor, name, index):
    if isinstance(descriptor, (StringProperty, TextProperty)):
        return "'%s_string'" % name
    if isinstance(descriptor, DateProperty):
        return "'1/%s/2014'" % (index + 1)
    if isinstance(descriptor, DateTimeProperty):
        return "'1/1/2014 01:%s:0'" % (index + 1)
    if isinstance(descriptor, (SimpleCurrency, SimpleDecimal)):
        return "'1.%s'" % (index + 1 if index >= 9 else '0%s' % (index + 1))
    if isinstance(descriptor, IntegerProperty):
        return "'%s'" % (index + 1)
    if isinstance(descriptor, FloatProperty):
        return "'1.%s'" % (index + 1)
    if isinstance(descriptor, BooleanProperty):
        return "'True'"


def _to_request_values(variable, descriptors_dct):
    template = "%(property)s=%(value)s"
    rendered = [template % {'variable': variable, 'property': p, 'value': _to_default_reques_value(descriptor, p, i)}
                for
                i, (p, descriptor) in
                enumerate(descriptors_dct.iteritems())]
    return ', '.join(rendered)


def _model_descriptors(app, model):
    model_class = _model_class(app, model)
    return {k: p for k, p in model_class._properties.iteritems() if k not in ['class', 'creation']}


def code_new_tests(app, model):
    descriptors_dct = _model_descriptors(app, model)
    model_underscore = _to_underscore_case(model)
    model_assertions = _to_model_assertions('saved_' + model_underscore, descriptors_dct)
    model_properties = ', '.join("'%s'" % k for k in descriptors_dct)
    request_values = _to_request_values('saved_' + model_underscore, descriptors_dct)
    return NEW_TESTS_TEMPLATE % {'app': app, 'model': model, 'model_underscore': model_underscore,
                                 'model_assertions': model_assertions, 'request_values': request_values,
                                 'model_properties': model_properties}


def code_edit_tests(app, model):
    descriptors_dct = _model_descriptors(app, model)
    model_underscore = _to_underscore_case(model)
    model_assertions = _to_model_assertions('edited_' + model_underscore, descriptors_dct)
    model_properties = ', '.join("'%s'" % k for k in descriptors_dct)
    request_values = _to_request_values('edited_' + model_underscore, descriptors_dct)
    return EDIT_TESTS_TEMPLATE % {'app': app, 'model': model, 'model_underscore': model_underscore,
                                  'model_assertions': model_assertions, 'request_values': request_values,
                                  'model_properties': model_properties}


def code_home_tests(app, model):
    model_underscore = _to_underscore_case(model)
    return HOME_TESTS_TEMPLATE % {'app': app, 'model': model, 'model_underscore': model_underscore}


def code_rest_tests(app, model):
    descriptors_dct = _model_descriptors(app, model)
    model_underscore = _to_underscore_case(model)
    model_assertions = _to_model_assertions('db_' + model_underscore, descriptors_dct)
    model_properties = ', '.join("'%s'" % k for k in descriptors_dct)
    request_values = _to_request_values('request_' + model_underscore, descriptors_dct)
    return REST_TESTS_TEMPLATE % {'app': app, 'model': model, 'model_underscore': model_underscore,
                                  'model_assertions': model_assertions, 'request_values': request_values,
                                  'model_properties': model_properties}



def init_new_tests(app, model):
    return generate_tests(app, model, 'new', code_new_tests)


def init_edit_tests(app, model):
    return generate_tests(app, model, 'edit', code_edit_tests)


def init_home_tests(app, model):
    return generate_tests(app, model, 'home', code_home_tests)


def init_rest_tests(app, model):
    return generate_tests(app, model, 'rest', code_rest_tests)


def scaffold(app, model, *properties):
    init_app(app, model, *properties)
    _title('commands.py')
    print init_commands(app, model)
    _title('facade.py')
    print init_facade(app, model)

    _title('creating routes folder')
    init_routes(app)
    _title('routes home.py')
    print init_home_script(app, model)

    _title('routes.new.py')
    print init_new_script(app, model)
    _title('routes.edit.py')
    print init_edit_script(app, model)
    _title('routes rest.py')
    print init_rest_script(app, model)
    _title('creating template folder ans base.html')
    init_html_templates(app)
    _title('templates/home.html')
    print init_home_html(app, model)

    _title('templates/form.html')
    print init_form_html(app, model)

    init_test(app, model)
    _title('creating new tests')
    print init_new_tests(app, model)
    _title('creating edit tests')
    print init_edit_tests(app, model)
    _title('creating home tests')
    print init_home_tests(app, model)
    _title('creating rest tests')
    print init_rest_tests(app, model)


def delete_app(app):
    flag = raw_input('Are you sure you want delete app %s (yes or no)? ' % app)
    if flag.lower() == 'yes':
        app_dir = os.path.join(APPS_DIR, app + '_app')
        shutil.rmtree(app_dir)

        template_dir = os.path.join(TEMPLATES_DIR, app + 's')
        shutil.rmtree(template_dir)

        web_dir = os.path.join(WEB_DIR, app + 's')
        shutil.rmtree(web_dir)

        test_dir = os.path.join(TEST_DIR, app + '_tests')
        shutil.rmtree(test_dir)


FUNC_DICT = {'model': init_app, 'app': scaffold, 'delete': delete_app}
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Commands available:'
        print '\n    '.join([''] + FUNC_DICT.keys())
        print 'both model or app must be folowed by <app> <model>'
    elif len(sys.argv) >= 3:
        fcn = FUNC_DICT.get(sys.argv[1])
        if fcn:
            fcn(*sys.argv[2:])
        else:
            print 'Invalid command: %s' % sys.argv[1]
    else:
        print 'Must use command %s followed by params: <app>  <model>' % sys.argv[1]



