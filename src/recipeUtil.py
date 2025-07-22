import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from constants import MEASUREMENTS, parse_ingredient

def auto_resize_popup(popup):
    """Automatically resize a popup window to fit its content."""
    popup.update_idletasks()  # Ensure all widgets are rendered
    popup.geometry(f"{popup.winfo_reqwidth()}x{popup.winfo_reqheight()}")

def add_recipe(root):
    import re  # Import regex for parsing numbers

    add_recipe_window = tk.Toplevel(root)
    add_recipe_window.title("Add Recipe")
    add_recipe_window.geometry("400x400")

    tk.Label(add_recipe_window, text="Recipe Name:").pack(pady=5)
    name_entry = tk.Entry(add_recipe_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(add_recipe_window, text="Ingredients (one per line):").pack(pady=5)
    ingredients_text = tk.Text(add_recipe_window, width=40, height=10)
    ingredients_text.pack(pady=5)

    def save_recipe():
        recipe_name = name_entry.get().strip()
        ingredients = ingredients_text.get("1.0", tk.END).strip().split("\n")

        if not recipe_name:
            messagebox.showerror("Error", "Recipe name cannot be empty.")
            return

        if not ingredients:
            messagebox.showerror("Error", "Ingredients cannot be empty.")
            return

        # Connect to the database
        conn = sqlite3.connect('mealMaestro_data.db')
        cursor = conn.cursor()

        # Insert recipe into the database
        cursor.execute('SELECT id FROM recipes WHERE name = ?', (recipe_name,))
        recipe = cursor.fetchone()
        if not recipe:
            cursor.execute('INSERT INTO recipes (name) VALUES (?)', (recipe_name,))
            recipe_id = cursor.lastrowid
        else:
            recipe_id = recipe[0]

        # Parse and insert ingredients
        for ingredient in ingredients:
            ingredient = ingredient.strip()

            # Check if the ingredient starts with a number
            match = re.match(r'^(\d+\.?\d*)\s*([a-zA-Z]*)\s*(.*)', ingredient)
            if match:
                quantity = match.group(1)  # Extract the quantity
                measurement = match.group(2)  # Extract the measurement
                ingredient_description = match.group(3)  # Extract the remaining description
            else:
                # If no number is found, treat the entire value as the description
                quantity = None
                measurement = None
                ingredient_description = ingredient

            # Insert ingredient into the database
            cursor.execute('''
                INSERT INTO ingredients (recipe_id, ingredient_description, quantity, measurement)
                VALUES (?, ?, ?, ?)
            ''', (recipe_id, ingredient_description, quantity, measurement))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Recipe added successfully.")
        add_recipe_window.destroy()

    tk.Button(add_recipe_window, text="Submit", command=save_recipe).pack(pady=10)

def view_recipe(root):
    # Create the popup window
    view_recipe_window = tk.Toplevel(root)
    view_recipe_window.title("View Recipe")
    view_recipe_window.geometry("400x400")

    # Fetch recipes from the database
    conn = sqlite3.connect('mealMaestro_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM recipes")
        recipes = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch recipe details: {e}")
        recipes = []
    finally:
        conn.close()

    # Dropdown to select a recipe
    selected_recipe = tk.StringVar(view_recipe_window)
    if recipes:
        selected_recipe.set(recipes[0])  # Set the first recipe as default
    else:
        selected_recipe.set("No recipes available")

    def load_recipe():
        recipe_name = selected_recipe.get()
        if recipe_name == "No recipes available":
            recipe_details.delete("1.0", tk.END)
            recipe_details.insert(tk.END, "No recipe details to display.")
        else:
            conn = sqlite3.connect('mealMaestro_data.db')
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    SELECT i.quantity, i.measurement, i.ingredient_description
                    FROM ingredients i
                    JOIN recipes r ON i.recipe_id = r.id
                    WHERE r.name = ?
                ''', (recipe_name,))
                ingredients = cursor.fetchall()
                print(f"Fetched ingredients for {recipe_name}: {ingredients}")  # Debugging output
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch recipe details: {e}")
                ingredients = []
            finally:
                conn.close()

            # Update the recipe details
            recipe_details.delete("1.0", tk.END)
            recipe_details.insert(tk.END, f"Recipe: {recipe_name}\n\nIngredients:\n")
            for quantity, measurement, description in ingredients:
                recipe_details.insert(tk.END, f"- {quantity or ''} {measurement or ''} {description}\n")

        # Automatically resize the popup to fit the updated content
        auto_resize_popup(view_recipe_window)

    dropdown = tk.OptionMenu(view_recipe_window, selected_recipe, *recipes)
    dropdown.pack(pady=5)

    # Submit button to load the selected recipe
    submit_button = tk.Button(view_recipe_window, text="View Recipe", command=load_recipe)
    submit_button.pack(pady=10)

    # Text widget to display the recipe details
    recipe_details = tk.Text(view_recipe_window, width=50, height=15, wrap="word")
    recipe_details.pack(pady=10)

    # Load the initial recipe details
    load_recipe()

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