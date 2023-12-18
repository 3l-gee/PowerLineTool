@echo off

REM Replace 'your_project_name' with the actual name of your Django project
set PROJECT_NAME=PowerlineTool

pip install pipenv
pause
pipenv run python -m pip install --upgrade pip
pause
pipenv install
pause

REM Open web browser with localhost:8000
start http://localhost:8000/map

REM Run Django development server
cd %PROJECT_NAME%
pipenv run python manage.py runserver
pause



