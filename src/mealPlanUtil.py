import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from collections import defaultdict
from constants import MEASUREMENTS, parse_ingredient
import xlwt  # Import xlwt for writing Excel files

# Function to create a meal plan
def create_meal_plan(root):
    def save_meal_plan():
        title = title_entry.get()
        selected_recipes = recipe_listbox.curselection()
        if title and selected_recipes:
            recipe_ids = ', '.join([str(recipe_list[i][0]) for i in selected_recipes])  # Get selected recipe IDs
            try:
                conn = sqlite3.connect('mealMaestro_data.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO meal_plans (title, recipe_ids)
                    VALUES (?, ?)
                ''', (title, recipe_ids))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Meal plan saved successfully!")
                create_meal_plan_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Meal plan title must be unique.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save meal plan: {e}")
        else:
            messagebox.showerror("Error", "Please enter a title and select at least one recipe.")

    def load_recipes():
        try:
            conn = sqlite3.connect('mealMaestro_data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM recipes')
            global recipe_list
            recipe_list = cursor.fetchall()
            conn.close()
            for recipe in recipe_list:
                recipe_listbox.insert(tk.END, recipe[1])  # Add recipe names to the listbox
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recipes: {e}")

    create_meal_plan_window = tk.Toplevel(root)
    create_meal_plan_window.title("Create Meal Plan")
    create_meal_plan_window.geometry("400x400")

    tk.Label(create_meal_plan_window, text="Meal Plan Title or Date:").pack(pady=5)
    title_entry = tk.Entry(create_meal_plan_window, width=30)
    title_entry.pack(pady=5)

    tk.Label(create_meal_plan_window, text="Select Recipes:").pack(pady=5)
    recipe_listbox = tk.Listbox(create_meal_plan_window, width=40, height=10, selectmode=tk.MULTIPLE)  # Allow multiple selection
    recipe_listbox.pack(pady=5)

    load_recipes()  # Load recipes into the listbox

    tk.Button(create_meal_plan_window, text="Save Meal Plan", command=save_meal_plan).pack(pady=10)

def generate_shopping_list(root):
    try:
        # Connect to the database
        conn = sqlite3.connect('mealMaestro_data.db')
        cursor = conn.cursor()

        # Fetch meal plans and recipes
        cursor.execute("SELECT title, recipe_ids FROM meal_plans")
        meal_plans = cursor.fetchall()

        if not meal_plans:
            messagebox.showerror("Error", "No meal plans found.")
            return

        # Create a workbook and add a sheet
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Shopping List")

        # Write headers
        sheet.write(0, 0, "Ingredient")
        sheet.write(0, 1, "Quantity")
        sheet.write(0, 2, "Measurement")
        sheet.write(0, 3, "Recipe Name")

        row = 1  # Start writing data from row 1

        for meal_plan in meal_plans:
            meal_plan_title = meal_plan[0]
            recipe_ids = meal_plan[1].split(", ")

            for recipe_id in recipe_ids:
                cursor.execute("SELECT name FROM recipes WHERE id = ?", (recipe_id,))
                recipe = cursor.fetchone()

                if recipe:
                    recipe_name = recipe[0]
                    cursor.execute("SELECT ingredient_description, quantity, measurement FROM ingredients WHERE recipe_id = ?", (recipe_id,))
                    ingredients = cursor.fetchall()

                    for ingredient_description, quantity, measurement in ingredients:
                        sheet.write(row, 0, ingredient_description)
                        sheet.write(row, 1, quantity)
                        sheet.write(row, 2, measurement)
                        sheet.write(row, 3, recipe_name)
                        row += 1

        # Save the workbook as an .xls file
        workbook.save("shopping_list.xls")
        messagebox.showinfo("Success", "Shopping list saved as shopping_list.xls")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate shopping list: {e}")
    finally:
        conn.close()


def generate_shopping_list_for_plan(selected_meal_plan, root):
    conn = None  # Initialize connection variable
    try:
        conn = sqlite3.connect('mealMaestro_data.db')
        cursor = conn.cursor()

        # Fetch the selected meal plan
        cursor.execute('SELECT title, recipe_ids FROM meal_plans WHERE title = ?', (selected_meal_plan,))
        meal_plan_data = cursor.fetchone()

        if not meal_plan_data:
            messagebox.showerror("Error", "Meal plan not found.")
            return

        meal_plan_title = meal_plan_data[0]  # Get the meal plan title
        recipe_ids = meal_plan_data[1].split(', ')  # Split comma-separated recipe IDs

        grouped_ingredients = defaultdict(list)
        recipe_titles = []

        # Fetch recipe names and ingredients
        for recipe_id in recipe_ids:
            cursor.execute('SELECT name FROM recipes WHERE id = ?', (recipe_id,))
            recipe_data = cursor.fetchone()
            if recipe_data:
                recipe_name = recipe_data[0]
                recipe_titles.append(recipe_name)  # Add recipe name to recipe titles

                # Fetch ingredients for the recipe
                cursor.execute('SELECT quantity, measurement, ingredient_description FROM ingredients WHERE recipe_id = ?', (recipe_id,))
                ingredients = cursor.fetchall()
                for quantity, measurement, description in ingredients:
                    normalized_ingredient = description.strip().lower()  # Normalize ingredient name
                    grouped_ingredients[normalized_ingredient].append((quantity, measurement, recipe_name))

        # Aggregate grouped ingredients
        aggregated_ingredients = defaultdict(list)
        for ingredient, details in grouped_ingredients.items():
            for quantity, measurement, recipe in details:
                aggregated_ingredients[ingredient].append((quantity, measurement, recipe))

        # Write shopping list to a text file
        with open("shopping_list.txt", "w") as file:
            file.write(f"Meal Plan Title: {meal_plan_title}\n")
            file.write(f"-----------------------\n")
            file.write("Recipes Included:\n")
            for recipe in recipe_titles:
                file.write(f"- {recipe}\n")
            file.write(f"\n************************************************\n")
            file.write("\nShopping List:\n")
            file.write(f"-------------------------\n")
            for ingredient, details in aggregated_ingredients.items():
                quantities_and_recipes = ", ".join([f"{quantity or ''} {measurement or ''} ({recipe})" for quantity, measurement, recipe in details])
                file.write(f"{ingredient}: {quantities_and_recipes}\n")

        messagebox.showinfo("Success", "Shopping list generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate shopping list: {e}")
    finally:
        if conn:
            conn.close()


    # Fetch all meal plan titles from the database
    conn = sqlite3.connect('mealMaestro_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM meal_plans')
    meal_plan_titles = [row[0] for row in cursor.fetchall()]
    conn.close()
