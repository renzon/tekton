Tekton
================

A full stack project for Google App Engine based on modules Tekton-micro, Gaegraph, Gaeforms and Gaepermission, Jinja2 and Babel

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
 
# python manager.py

manager.py is Tekton’s command-line utility for code generation. 

## Commands available

- model
- app
- delete

### app

It's possible to determine the app creation, specifying the name and the central entity from the module. Example:

``` python manager.py app course Course title:string price:currency begin:date ```

- int: integer number.
- float: floating-point number.
- decimal: floating-point number with 2 decimal precision.
- currency: money with 2 decimal precision.
- string: string of characters
- date: day, month and year.
- datetime: day, month, year, hour, minutes and seconds.

# Contributors:

* [Denis Costa](https://github.com/deniscostadsc)
* [Lucas Campos](https://github.com/willianribeiro)
* [Tony Lâmpada](https://github.com/tonylampada)
* [Willian Ribeiro](https://github.com/willianribeiro)
* [Guido Percú](https://github.com/GuidoBR)
