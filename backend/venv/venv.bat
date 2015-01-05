call :to_console "Setting up virtualenv on venv"

cd %~dp0 || goto :error

call :to_console "creating virtual env on venv folder"
virtualenv . || goto :error 

call :to_console "Activating virtualenv"
call Scripts\activate || goto :error 


IF "%1"=="" (
call :to_console "Checking up dependencies"
pip install -r dev_requirements.txt --upgrade || goto :error
) ELSE (
call :to_console "Checking up dependencies with proxy %1"
pip install -r dev_requirements.txt --upgrade --proxy=%1 || goto :error
)
cd ..\appengine || goto :error

IF EXIST %cd%\lib (
rmdir %cd%\lib
)

call :to_console "Creating symlink on plugins\appengine so installed libs become visible to Google App Engine"
MKLINK /D lib ..\venv\Lib\site-packages

IF EXIST %cd%\apps (
rmdir %cd%\apps
)

call :to_console "Creating symlink on plugins\appengine so apps become visible to Google App Engine"
MKLINK /D apps ..\apps


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