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
                    name TEXT NOT NULL,
                    ingredients TEXT NOT NULL
                )
            ''')
            with open(file_path, 'r') as file:
                for line in file:
                    # Each line should be in the format: Recipe Name|Ingredient1; Ingredient2; Ingredient3
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        name = parts[0].strip()
                        ingredients = parts[1].strip()  # Ingredients are separated by semicolons
                        cursor.execute('''
                            INSERT INTO recipes (name, ingredients)
                            VALUES (?, ?)
                        ''', (name, ingredients))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Recipes loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recipes: {e}")

    file_path = filedialog.askopenfilename(
        title="Select Recipe File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        parse_and_save_recipes(file_path)
        
# Create the main application window
root = tk.Tk()
root.title("Load Recipes")
root.geometry("400x200")

# Add button to load recipes from file
load_recipes_button = tk.Button(root, text="Load Recipes from File", command=load_recipes_from_file)
load_recipes_button.pack(pady=20)

# Add exit button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

# Start the tkinter main event loop
root.mainloop()