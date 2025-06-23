import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from constants import MEASUREMENTS, parse_ingredient

def add_recipe(root):
    add_recipe_window = tk.Toplevel(root)
    add_recipe_window.title("Add Recipe")
    add_recipe_window.geometry("400x400")

    tk.Label(add_recipe_window, text="Recipe Name:").pack(pady=5)
    name_entry = tk.Entry(add_recipe_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(add_recipe_window, text="Ingredients (quantity | measurement | description, one per line):").pack(pady=5)
    ingredients_text = tk.Text(add_recipe_window, width=40, height=10)
    ingredients_text.pack(pady=5)

    def save_recipe():
        name = name_entry.get().strip()
        ingredients = ingredients_text.get("1.0", tk.END).strip()

        if name and ingredients:
            conn = None
            try:
                conn = sqlite3.connect('mealMaestro_data.db')
                cursor = conn.cursor()

                cursor.execute('INSERT INTO recipes (name) VALUES (?)', (name,))
                recipe_id = cursor.lastrowid

                for line in ingredients.splitlines():
                    if line.strip():
                        quantity, measurement, description = parse_ingredient(line)
                        cursor.execute('INSERT INTO ingredients (recipe_id, quantity, measurement, ingredient_description) VALUES (?, ?, ?, ?)',
                                       (recipe_id, quantity, measurement, description))

                conn.commit()
                messagebox.showinfo("Success", "Recipe added successfully!")
                add_recipe_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Recipe name must be unique.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add recipe: {e}")
            finally:
                if conn:
                    conn.close()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    tk.Button(add_recipe_window, text="Submit", command=save_recipe).pack(pady=10)

def view_recipe(root):
    def show_recipe_details(selected_recipe):
        try:
            conn = sqlite3.connect('mealMaestro_data.db')
            cursor = conn.cursor()
            
            # Fetch the selected recipe details
            cursor.execute('SELECT id, name FROM recipes WHERE name = ?', (selected_recipe,))
            recipe_data = cursor.fetchone()
            
            if not recipe_data:
                messagebox.showerror("Error", "Recipe not found.")
                return
            
            recipe_id = recipe_data[0]
            recipe_name = recipe_data[1]

            # Fetch ingredients for the recipe
            cursor.execute('SELECT quantity, ingredient_description FROM ingredients WHERE recipe_id = ?', (recipe_id,))
            ingredients = cursor.fetchall()

            # Update the labels with the recipe details
            recipe_name_label.config(text=f"Recipe Name: {recipe_name}")
            recipe_ingredients_label.config(text="Ingredients:\n" + "\n".join(
                [f"{quantity or ''} {description}" for quantity, description in ingredients]
            ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch recipe details: {e}")
        finally:
            conn.close()

    # Create a new window for selecting and viewing a recipe
    view_recipe_window = tk.Toplevel(root)
    view_recipe_window.title("View Recipe")
    view_recipe_window.geometry("400x400")

    tk.Label(view_recipe_window, text="Select a Recipe:").pack(pady=10)

    # Fetch all recipe names from the database
    conn = sqlite3.connect('mealMaestro_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM recipes')
    recipe_names = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Handle empty recipe list
    if not recipe_names:
        recipe_names = ["No Recipes Available"]

    # Dropdown menu for selecting a recipe
    selected_recipe = tk.StringVar(view_recipe_window)
    selected_recipe.set(recipe_names[0])  # Set the default value
    recipe_dropdown = tk.OptionMenu(view_recipe_window, selected_recipe, *recipe_names)
    recipe_dropdown.pack(pady=10)

    # Button to fetch and display the recipe details
    tk.Button(view_recipe_window, text="View Recipe", command=lambda: show_recipe_details(selected_recipe.get())).pack(pady=10)

    # Labels to display the recipe details
    recipe_name_label = tk.Label(view_recipe_window, text="Recipe Name: ", font=("Arial", 14))
    recipe_name_label.pack(pady=10)

    recipe_ingredients_label = tk.Label(view_recipe_window, text="Ingredients:", font=("Arial", 12), justify="left", wraplength=350)
    recipe_ingredients_label.pack(pady=10)

def delete_recipe(root):
    # Create a new window for deleting a recipe
    delete_recipe_window = tk.Toplevel(root)
    delete_recipe_window.title("Delete Recipe")
    delete_recipe_window.geometry("400x300")

    tk.Label(delete_recipe_window, text="Select a Recipe to Delete:", font=("Arial", 12)).pack(pady=10)

    # Fetch all recipe names from the database
    conn = sqlite3.connect('mealMaestro_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM recipes')
    recipe_names = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Handle empty recipe list
    if not recipe_names:
        recipe_names = ["No Recipes Available"]

    # Dropdown menu for selecting a recipe
    selected_recipe = tk.StringVar(delete_recipe_window)
    selected_recipe.set(recipe_names[0])  # Set the default value
    recipe_dropdown = tk.OptionMenu(delete_recipe_window, selected_recipe, *recipe_names)
    recipe_dropdown.pack(pady=10)

    def confirm_delete():
        recipe_to_delete = selected_recipe.get()
        if recipe_to_delete != "No Recipes Available":
            try:
                conn = sqlite3.connect('mealMaestro_data.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM recipes WHERE name = ?', (recipe_to_delete,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Recipe '{recipe_to_delete}' deleted successfully!")
                delete_recipe_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete recipe: {e}")
        else:
            messagebox.showerror("Error", "No recipe selected to delete.")

    # Add a button to confirm deletion
    delete_button = tk.Button(delete_recipe_window, text="Delete Recipe", command=confirm_delete)
    delete_button.pack(pady=10)

    # Add a button to close the window
    close_button = tk.Button(delete_recipe_window, text="Cancel", command=delete_recipe_window.destroy)
    close_button.pack(pady=10)

def edit_recipe(root):
    def save_edited_recipe(selected_recipe, new_name, new_ingredients):
        try:
            conn = sqlite3.connect('mealMaestro_data.db')
            cursor = conn.cursor()

            # Update the recipe name in the database
            cursor.execute('UPDATE recipes SET name = ? WHERE name = ?', (new_name, selected_recipe))

            # Fetch the recipe ID for the updated recipe
            cursor.execute('SELECT id FROM recipes WHERE name = ?', (new_name,))
            recipe_id = cursor.fetchone()[0]

            # Delete old ingredients for the recipe
            cursor.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))

            # Insert updated ingredients into the database
            for line in new_ingredients.splitlines():
                if line.strip():
                    quantity, measurement, description = parse_ingredient(line)
                    cursor.execute('INSERT INTO ingredients (recipe_id, quantity, measurement, ingredient_description) VALUES (?, ?, ?, ?)',
                                   (recipe_id, quantity, measurement, description))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Recipe updated successfully!")
            edit_recipe_window.destroy()  # Close the edit window after success
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update recipe: {e}")

    def load_existing_ingredients(selected_recipe):
        try:
            conn = sqlite3.connect('mealMaestro_data.db')
            cursor = conn.cursor()

            # Fetch the recipe ID for the selected recipe
            cursor.execute('SELECT id FROM recipes WHERE name = ?', (selected_recipe,))
            recipe_data = cursor.fetchone()

            if not recipe_data:
                messagebox.showerror("Error", "Recipe not found.")
                return

            recipe_id = recipe_data[0]

            # Fetch existing ingredients for the recipe
            cursor.execute('SELECT quantity, measurement, ingredient_description FROM ingredients WHERE recipe_id = ?', (recipe_id,))
            ingredients = cursor.fetchall()
            conn.close()

            # Populate the ingredients text area with the existing ingredients
            ingredients_text.delete("1.0", tk.END)  # Clear the text area
            for quantity, measurement, description in ingredients:
                ingredients_text.insert(tk.END, f"{quantity or ''} {measurement or ''} {description}\n")

            # Default the current recipe name into the "New Recipe Name" entry box
            new_name_entry.delete(0, tk.END)  # Clear the entry box
            new_name_entry.insert(0, selected_recipe)  # Insert the selected recipe name
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ingredients: {e}")

    # Create a new window for selecting and editing a recipe
    edit_recipe_window = tk.Toplevel(root)
    edit_recipe_window.title("Edit Recipe")
    edit_recipe_window.geometry("400x600")

    tk.Label(edit_recipe_window, text="Select a Recipe:").pack(pady=10)

    # Fetch all recipe names from the database
    conn = sqlite3.connect('mealMaestro_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM recipes')
    recipe_names = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Handle empty recipe list
    if not recipe_names:
        recipe_names = ["No Recipes Available"]

    # Dropdown menu for selecting a recipe
    selected_recipe = tk.StringVar(edit_recipe_window)
    selected_recipe.set(recipe_names[0])  # Set the default value
    recipe_dropdown = tk.OptionMenu(edit_recipe_window, selected_recipe, *recipe_names)
    recipe_dropdown.pack(pady=10)

    # Load existing ingredients when a recipe is selected
    tk.Button(edit_recipe_window, text="Load Ingredients", command=lambda: load_existing_ingredients(selected_recipe.get())).pack(pady=5)

    tk.Label(edit_recipe_window, text="New Recipe Name:").pack(pady=5)
    new_name_entry = tk.Entry(edit_recipe_window, width=30)
    new_name_entry.pack(pady=5)

    tk.Label(edit_recipe_window, text="Ingredients (quantity | measurement | description, one per line):").pack(pady=5)
    ingredients_text = tk.Text(edit_recipe_window, width=40, height=10)
    ingredients_text.pack(pady=5)

    # Button to save the edited recipe
    tk.Button(edit_recipe_window, text="Save Changes", command=lambda: save_edited_recipe(selected_recipe.get(), new_name_entry.get(), ingredients_text.get("1.0", tk.END).strip())).pack(pady=10)