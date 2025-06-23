# Meal Maestro

Meal Maestro is a Python-based recipe management application that allows users to add, edit, delete, and view recipes. It also generates shopping lists based on selected meal plans, grouping like ingredients together for convenience.

## Features
- Add recipes (bulk or one ingredient at a time).
- Edit existing recipes.
- Delete recipes.
- View recipes and their ingredients.
- Generate shopping lists grouped by ingredients and recipes.

## How to Build and Run

### Prerequisites
1. Install Python 3.9 or later.
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt

### Requirements
- pyinstaller


### Run locally
   python mealMaestro.py


### Build Deployable executable
1. From the /src directory, run
   pyinstaller --onefile --add-data "recipes_load.txt;." --add-data "recipes_dump.txt;." mealMaestro.py


### Run Executable
   cd dist
   ./mealMaestro.exe

   
### Create Database
   python setupDb.py

### Delete Database
   python deleteDb.py
