# PowerLineTool
the goal of this too is to allow a user to select, merge, combine powerline data. 


VirutualEnv 
```bash
cd your-project

python -m venv venv // pip install virtualenv

.\venv\Scripts\activate

pip install -r requirements.txt

cd PowerlineTool

python manage.py runserver

start http://localhost:8000/map
```

Once the map is displayed in the webbrowser :

STEP 1 : The goal is to select the dataset of data to work with
- DCS : Loads a dcs feature 
  - Chose File (DCSexemple.json)
  - Save
  - DCS feature is added to the features
- Map click
    - Displays clicked features
    - ( + ) loads a feature
    - TLM feature is added to the features
- ( - ) deletes a feature
- RESET : emptys the features
- VALIDATE (at least one feature), opens step 2

STEP 2 : we can now modify the data
- left click point : show detail
- left click line : show detail + 3 history entry
- right click point : Fuse or divde 
- fuse : both ends
-  divide : in between
    - unwanted part can be deletd with ( - )
- EXPORT : TODO Export



