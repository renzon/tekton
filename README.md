Tekton
================

A full stack project for Google App Engine based on modules [Tekton-micro](https://github.com/renzon/tekton-micro), 
[Gaegraph](https://github.com/renzon/gaegraph), [Gaeforms](https://github.com/renzon/gaeforms) and [Gaepermission](https://github.com/renzon/gaepermission), Jinja2 and Babel

This application is running on <https://tekton-fullstack.appspot.com>

1. [Book App Engne and Python in pt_BR](https://leanpub.com/appengine)
2. [Vìdeos about the project in pt_BR](https://www.youtube.com/playlist?list=PLA05yVJtRWYRGIeBxag8uT-3ftcMVT5oF)

# Installation:
* Install [Google App Engine SDK](https://cloud.google.com/appengine/downloads)
* Download the tekton source code
* Run venv.sh to create virtual env
```  cd backend/venv && ./venv.sh (venv.bat if you use Windows) ```
* Virtualenv
``` source ./bin/activate ```
* Execute server on backend/appengine folder
```  cd ../appengine && dev_appserver.py . ```
* See if it works on ```http://localhost:8080```

# Contributors:

* [Denis Costa](https://github.com/deniscostadsc)
* [Lucas Campos](https://github.com/willianribeiro)
* [Tony Lâmpada](https://github.com/tonylampada)
* [Willian Ribeiro](https://github.com/willianribeiro)
* [Guido Percú](https://github.com/GuidoBR)
