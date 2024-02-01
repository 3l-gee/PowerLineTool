@echo off

python -m venv venv
pause
call venv\Scripts\activate
pause
pip install -r requirements.txt
pause
start http://localhost:8000/map
python PowerlineTool/manage.py runserver
pause



