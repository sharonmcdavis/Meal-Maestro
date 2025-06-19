import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from setupDb import setup_database  # Import the setup_database function
from fileUtil import load_recipes_from_file, dump_recipes_to_file  # Import file utility functions
from recipeUtil import add_recipe, bulk_add_recipe, view_recipe, edit_recipe
from mealPlanUtil import create_meal_plan, generate_shopping_list

# Call setup_database to initialize the database
setup_database()

# Create the main window
root = tk.Tk()
root.title("Recipe Database")

# Set the window size
root.geometry("500x650")

# Add a label to the window
label = tk.Label(root, text="Welcome to the Sharon's Recipe Database!", font=("Arial", 16))
label.pack(pady=20)

label = tk.Label(root, text="Recipe Management:", font=("Arial", 12))
label.pack(pady=20)

add_recipe_button = tk.Button(root, text="Add Recipe", command=lambda: add_recipe(root))
add_recipe_button.pack(pady=5)

bulk_add_recipe_button = tk.Button(root, text="Bulk Add Recipe", command=lambda: bulk_add_recipe(root))
bulk_add_recipe_button.pack(pady=5)

view_recipe_button = tk.Button(root, text="View Recipe", command=lambda: view_recipe(root))
view_recipe_button.pack(pady=5)

edit_recipe_button = tk.Button(root, text="Edit Recipe", command=lambda: edit_recipe(root))
edit_recipe_button.pack(pady=5)

label = tk.Label(root, text="Meal Plan Management:", font=("Arial", 12))
label.pack(pady=20)

create_meal_plan_button = tk.Button(root, text="Create Meal Plan", command=lambda: create_meal_plan(root))
create_meal_plan_button.pack(pady=5)

generate_shopping_list_button = tk.Button(root, text="Generate Shopping List", command=lambda: generate_shopping_list(root))
generate_shopping_list_button.pack(pady=5)

label = tk.Label(root, text="Import/Export Recipes:", font=("Arial", 12))
label.pack(pady=20)

# Add button to load recipes from file
load_recipes_button = tk.Button(root, text="Load Recipes from File", command=load_recipes_from_file)
load_recipes_button.pack(pady=5)

dump_recipes_button = tk.Button(root, text="Dump Recipes to File", command=dump_recipes_to_file)
dump_recipes_button.pack(pady=5)

# Add a button to close the window
close_button = tk.Button(root, text="Exit", command=root.quit)
close_button.pack(pady=5)

# Run the GUI event loop
root.mainloop()