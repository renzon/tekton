call :to_console "Setting up virtualenv on venv"

call :to_console "creating virtual env on venv folder"
virtualenv . || goto :error 

call :to_console "Activating virtualenv"
call Scripts\activate || goto :error 


call :to_console "Checking up dependencies"

pip install -r dev_requirements.txt --upgrade || goto :error 


cd ..\appengine || goto :error

IF NOT EXIST %cd%\lib (
call :to_console "Creating symlink on plugins\appengine so installed libs become visible to Google App Engine"
MKLINK /D lib ..\venv\Lib\site-packages
)

IF NOT EXIST %cd%\apps (
call :to_console "Creating symlink on plugins\appengine so apps become visible to Google App Engine"
MKLINK /D apps ..\apps
)


cd ..\venv || goto :error
call :to_console "virtualenv and dependencies installed"
goto:EOF


:to_console 
echo "------------ %~1  -----------"
goto:EOF

:error
call :to_console Failed with error #%errorlevel%.
exit /b %errorlevel%
goto:EOF