import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import sqlite3

def load_recipes_from_file():
    try:
        # Prompt user to select the file
        file_path = filedialog.askopenfilename(
            title="Select Recipe File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        conn = sqlite3.connect('recipe_database.db')
        cursor = conn.cursor()

        # Ensure tables exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                quantity TEXT,
                ingredient_description TEXT NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        ''')

        # Read and parse the file
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    recipe_name = parts[0].strip()
                    ingredients = parts[1].strip().split(';')
                    
                    # Insert recipe into the database
                    cursor.execute('INSERT OR IGNORE INTO recipes (name) VALUES (?)', (recipe_name,))
                    recipe_id = cursor.lastrowid

                    # Insert ingredients into the database
                    for ingredient in ingredients:
                        ingredient_parts = ingredient.strip().split(' ', 1)
                        quantity = ingredient_parts[0].strip() if len(ingredient_parts) > 1 else None
                        description = ingredient_parts[1].strip() if len(ingredient_parts) > 1 else ingredient_parts[0].strip()
                        cursor.execute('INSERT INTO ingredients (recipe_id, quantity, ingredient_description) VALUES (?, ?, ?)',
                                       (recipe_id, quantity, description))
                else:
                    print(f"Invalid line format: {line.strip()}")

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Recipes loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load recipes: {e}")

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