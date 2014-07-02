import json
import jinja2
from jinja2._markupsafe import Markup
from webapp2_extras import i18n
import os

_base = os.path.dirname(__file__)
_base = os.path.join(_base, '..')
_base = os.path.normpath(_base)
_base_2 = os.path.join(_base, 'templates')
_jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader([_base_2]),
    trim_blocks=True,
    autoescape=True,
    extensions=['jinja2.ext.i18n'])

_jinja_environment.install_gettext_translations(i18n)


def _json_escaped(value):
    return Markup(json.dumps(value))


_jinja_environment.filters['json'] = _json_escaped


def render(template_name, values={}):
    template = _jinja_environment.get_template(template_name)
    return template.render(values)

