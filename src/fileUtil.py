import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

def load_recipes_from_file():
    def parse_and_save_recipes(file_path):
        try:
            conn = sqlite3.connect('recipe_database.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    ingredients TEXT NOT NULL
                )
            ''')
            conn.commit()  # Commit table creation to release lock
            
            with open(file_path, 'r') as file:
                for line in file:
                    # Each line should be in the format: Recipe Name|Ingredient1, Ingredient2, Ingredient3
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        name = parts[0].strip()
                        ingredients = parts[1].strip()
                        try:
                            cursor.execute('''
                                INSERT INTO recipes (name, ingredients)
                                VALUES (?, ?)
                            ''', (name, ingredients))
                        except sqlite3.IntegrityError:
                            messagebox.showerror("Error", f"Duplicate recipe name: {name}")
            conn.commit()  # Commit inserts to release lock
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error", f"Database is locked: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recipes: {e}")
        finally:
            conn.close()  # Ensure the connection is closed

    file_path = filedialog.askopenfilename(
        title="Select Recipe File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        parse_and_save_recipes(file_path)

def dump_recipes_to_file():
    try:
        conn = sqlite3.connect('recipe_database.db')
        cursor = conn.cursor()
        
        # Fetch all recipes from the database
        cursor.execute('SELECT name, ingredients FROM recipes')
        recipes = cursor.fetchall()
        conn.close()
        
        # Write recipes to a file with semicolon as the ingredient delimiter
        with open("recipes_dump.txt", "w") as file:
            for recipe in recipes:
                file.write(f"{recipe[0]}|{recipe[1].replace(',', ';')}\n")  # Replace commas with semicolons
        
        messagebox.showinfo("Success", "Recipes dumped to recipes_dump.txt successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to dump recipes: {e}")
        

