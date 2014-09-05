# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import shutil
import sys
import os


def patch(system):
    def sys(cmd):
        print cmd
        return system(cmd)

    return sys


os.system = patch(os.system)

# workaround to add src to path
babel_dir = os.path.dirname(__file__)
logging.info("babel dir: %s" % babel_dir)
proj_dir = os.path.join(babel_dir, "..", '..')
proj_dir = os.path.normpath(proj_dir)
logging.info("project dir: %s" % proj_dir)
sys.path.append(os.path.join(proj_dir, 'src'))
if 'GAE_SDK' in os.environ:
    SDK_PATH = os.environ['GAE_SDK']

    sys.path.insert(0, SDK_PATH)

    import dev_appserver

    dev_appserver.fix_sys_path()

import settings


def create_or_update_catalog(loc, compile_target, msgs_pot):
    result = os.system("pybabel update -l %s -d %s -i %s" % (loc, compile_target, msgs_pot))
    if result != 0:
        os.system("pybabel init -l %s -d %s -i %s" % (loc, compile_target, msgs_pot))


def compile_po_files(compile_target, locale_target):
    for root, dirs, files in os.walk(compile_target):
        file_name = "messages.po" if "messages.po" in files else None
        if file_name:
            po_file = os.path.join(root, file_name)
            mo_dir = root.replace(os.path.join('.', 'locale'), locale_target)
            mo_file = os.path.join(mo_dir, "messages.mo")
            if not os.path.exists(mo_dir):
                os.makedirs(mo_dir)
                print "Created dir: %s" % mo_dir

            c = "pybabel compile -f -i %s -o %s " % (po_file, mo_file)
            print c
            os.system(c)


if __name__ == "__main__":
    compile_target = os.path.join(".", "locale")
    target = os.path.join(proj_dir, 'appengine')
    if os.path.sep == r'/':
        compile_targets = target + ' ' + os.path.join(proj_dir, "venv")
    else:
        compile_targets = target
    # if len(sys.argv) == 1:
    babel_cfg = os.path.join(babel_dir, "babel.cfg")
    msgs_pot = os.path.join(compile_target, "messages.pot")
    os.system("pybabel extract -F %s -o %s %s" % (babel_cfg, msgs_pot, compile_targets))
    locales = settings.LOCALES
    for loc in locales:
        create_or_update_catalog(loc, compile_target, msgs_pot)

    locale_target = os.path.join(target, "locale")
    compile_po_files(compile_target, locale_target)
