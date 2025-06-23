import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import sqlite3

def load_recipes_from_file():
    try:
        # Determine the correct path for recipes_load.txt
        if getattr(sys, 'frozen', False):  # Check if running as an executable
            base_path = sys._MEIPASS  # Path to the temporary directory for bundled files
        else:
            base_path = os.path.dirname(__file__)  # Path to the script directory

        file_path = os.path.join(base_path, "recipes_load.txt")

        # Load recipes from the file
        conn = sqlite3.connect('recipe_database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                ingredients TEXT NOT NULL
            )
        ''')
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    name = parts[0].strip()
                    ingredients = parts[1].strip().replace(';', '\n')  # Replace semi-colons with newlines
                    try:
                        cursor.execute('''
                            INSERT INTO recipes (name, ingredients)
                            VALUES (?, ?)
                        ''', (name, ingredients))
                    except sqlite3.IntegrityError:
                        print(f"Duplicate recipe name: {name}")
        conn.commit()
        conn.close()
        print("Recipes loaded successfully!")
    except Exception as e:
        print(f"Failed to load recipes: {e}")

def dump_recipes_to_file():
    try:
        # Determine the correct path for recipes_dump.txt
        if getattr(sys, 'frozen', False):  # Check if running as an executable
            base_path = os.path.dirname(sys.executable)  # Path to the directory containing main.exe
        else:
            base_path = os.path.dirname(__file__)  # Path to the script directory

        file_path = os.path.join(base_path, "recipes_dump.txt")

        # Fetch all recipes from the database
        conn = sqlite3.connect('recipe_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, ingredients FROM recipes')
        recipes = cursor.fetchall()

        # Write recipes to the file
        with open(file_path, 'w') as file:
            for recipe in recipes:
                file.write(f"{recipe[0]}|{recipe[1]}\n")
        print(f"Recipes dumped successfully to {file_path}!")
    except Exception as e:
        print(f"Failed to dump recipes: {e}")