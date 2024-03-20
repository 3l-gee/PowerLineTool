# PowerLineTool

## Installation

```bash
cd your-project

python -m venv venv // pip install virtualenv

.\venv\Scripts\activate

pip install -r requirements.txt

cd PowerlineTool

python manage.py runserver

start http://localhost:8000/map
```
## Story time

The Swiss air navigation obstacle data set is inaccurate with regards to powerlines (https://s.geo.admin.ch/r9l8c3vzakuh). 
 - Poles are missing
 - Line heights are missing
 - Positions are inacurates
 - There are topological mistakes.

Swisstopo was requested to conduct a lidar survey to address the data set issue. The survey was conducted as part of their TLM datasets, which can be found at https://www.swisstopo.admin.ch/fr/modele-du-territoire-swisstlm3d. The survey covered all referenced powerlines in Switzerland, as documented in _TLMFullFeatures.json._

Automatic updating of the current data set with the newer one was not allowed, as it would change the published tracing of the obstacle, thereby voiding the approval letter given as a legal obligation to the owner. 
Swisstopo did not consider this during their digitisation of the powerline datasets.
The issue will ultimately be resolved, and we will replace the entire dataset at a later date. 

While we can't change the tracing (A - B - C) => (A - B) and (B - C) we are allowd to update the information about the tracing : (A - B) => (A - B) :
This means that lines must be combined, divided, shortened, or extended.

## Requirements

- ✔️ Ingest TLM dataset
- ✔️ Ingest DCS feature
- ❌ Ingest CSV feature
- ✔️ merge
- ✔️ divide
- ✔️ cut
- ✔️ traceability of changes
- ✔️ export


## Use case

STEP 1 : The goal is to select the dataset of data to work with
- DCS : Loads a dcs feature 
  - Chose File to load the geometry from (DCSexemple.json)
  - Save
  - DCS feature is added to the features
- Map Single click
    - Displays clicked feature
    - ( ADD ) loads a feature
    - TLM feature is added to the features
- Map Double click
    - Displays all clicked features
    - ( ADD ) loads a feature
    - TLM feature is added to the features
- ( REMOVE ) deletes a feature
- RESET : emptys the features
- VALIDATE (at least one feature), opens step 2

STEP 2 : we can now modify the data
- left Single click point : show detail
- left Single click line : show detail + 3 history entry
- left Double click : shows all the selected features detail + 3 history entry
- right click point : Fuse or divde 
  - fuse : both ends
  - divide : in between
    - unwanted part can be deletd with ( REMOVE )
- EXPORT : Export the geoemtry
  - Chose File to load the metadata from (DCSexemple.json)
  - Save
  - Two files are downloaded:
  - History : shows all the steps undertaken to change the feature
  - MOD: shows all the finished geometry

## Generic View
- <span style="color:red">**Blue**<span>: TLM data set (loaded automatically)
- <span style="color:blue">**Red**<span> : DCS feature / CSV feature
![image](https://github.com/3l-gee/PowerLineTool/assets/124341972/a42060b8-a1a7-4240-87db-7615a511eed4)

## Precise View
- **🔻 Red Triangle** : Start of a line
- **🔹 Blue Triangle** : End of a line
- **❌ Red Symbol** : Other Obstacle 
- **➖ Blue Line** : Powerline Obstacle
![image](https://github.com/3l-gee/PowerLineTool/assets/124341972/d042bcdc-bc64-40bf-be6e-28e5d6be81ba)

## Feature information
- A selected feature can display information with a left click
- **Source** : The current name of the feature
- **History** : the 3 last history entries
- **CTRL** : nodes / edges 
![image](https://github.com/3l-gee/PowerLineTool/assets/124341972/36826edd-454e-4420-a92e-b4c04a208674)

## Stage 1 Selection / Select a TLM Feature to use 
- Left Click on line
- It is pink highlighted
- "+" to add it to the loaded features
- It gets added to the list of selected features
![image](https://github.com/3l-gee/PowerLineTool/assets/124341972/dc8e1a58-b4aa-4ca8-9f2f-a44bc574c82c)

## Stage 2 Formatting / Division
- Right click a point
- Divde option opens up
- Division creates two new segement of the same line divided at this point
![image](https://github.com/3l-gee/PowerLineTool/assets/124341972/5afbe653-ae7c-4a14-84d0-8d6e02bb31fb)

## Stage 2 Formatting / Fuse
- Right click a point that is the last point of two segement allow it to fuse
- Fuse is allowed if the distance btweent two point is not greater then 0.1m
- Both lines will fuse and produce one fused line
![image](https://github.com/3l-gee/PowerLineTool/assets/124341972/51914691-6c62-442c-93e7-3bd8b692e2f3)

