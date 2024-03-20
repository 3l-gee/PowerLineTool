@echo off

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
start http://localhost:8000/map
python PowerlineTool/manage.py runserver



