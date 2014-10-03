#!/bin/bash

set -e  # If occur any error, exit

function to_console {
    echo -e "\n*** $1 ***\n"
}

cd $(dirname $0) && cd ..

to_console "creating virtual env on venv folder"
virtualenv -p /usr/bin/python2.7 venv

to_console "Activating virtualenv"
source venv/bin/activate

to_console "Checking up dependencies"
if [ ! -z "$1" ]
    then
        to_console "Running with proxy "$1
        pip install -r venv/dev_requirements.txt --proxy=$1
    else
        to_console 'Runing with no proxy'
        pip install -r venv/dev_requirements.txt
fi

cd appengine

if [ ! -d lib ]; then
    to_console "Creating symlink on plugins/appengine/lib so installed libs become visible to Google App Engine"
    ln -s ../venv/lib/python2.7/site-packages lib
fi

if [ ! -d apps ]; then
    to_console "Creating symlink on plugins/appengine/apps so apps become visible to Google App Engine"
    ln -s ../apps apps
fi

