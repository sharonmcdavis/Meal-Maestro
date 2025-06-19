import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

# Function to create a meal plan
def create_meal_plan(root):
    def save_meal_plan():
        title = title_entry.get()
        selected_recipes = recipe_listbox.curselection()
        if title and selected_recipes:
            recipe_ids = ', '.join([str(recipe_list[i][0]) for i in selected_recipes])  # Get selected recipe IDs
            try:
                conn = sqlite3.connect('recipe_database.db')
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
            conn = sqlite3.connect('recipe_database.db')
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

# Function to generate a shopping list
def generate_shopping_list(root):
    def save_shopping_list(selected_meal_plan):
        try:
            conn = sqlite3.connect('recipe_database.db')
            cursor = conn.cursor()
            
            # Fetch the selected meal plan
            cursor.execute('SELECT title, recipe_ids FROM meal_plans WHERE title = ?', (selected_meal_plan,))
            meal_plan_data = cursor.fetchone()
            
            if not meal_plan_data:
                messagebox.showerror("Error", "Meal plan not found.")
                return
            
            meal_plan_title = meal_plan_data[0]  # Get the meal plan title
            recipe_ids = meal_plan_data[1].split(', ')  # Split comma-separated recipe IDs
            
            shopping_list = {}
            recipe_titles = []

            # Fetch recipe names and ingredients
            for recipe_id in recipe_ids:
                cursor.execute('SELECT name, ingredients FROM recipes WHERE id = ?', (recipe_id,))
                recipe_data = cursor.fetchone()
                if recipe_data:
                    recipe_name = recipe_data[0]
                    recipe_titles.append(recipe_name)  # Add recipe name to recipe titles
                    ingredients = recipe_data[1].split(', ')  # Split comma-separated ingredients
                    for ingredient in ingredients:
                        if ingredient in shopping_list:
                            shopping_list[ingredient].append(recipe_name)
                        else:
                            shopping_list[ingredient] = [recipe_name]
            
            # Write shopping list to a text file
            with open("shopping_list.txt", "w") as file:
                file.write(f"Meal Plan Title: {meal_plan_title}\n")
                file.write("Recipes Included:\n")
                for recipe in recipe_titles:
                    file.write(f"- {recipe}\n")
                file.write("\nShopping List:\n")
                for ingredient, recipes in shopping_list.items():
                    file.write(f"- {ingredient} ({', '.join(recipes)})\n")
            
            messagebox.showinfo("Success", "Shopping list generated successfully!")
            select_meal_plan_window.destroy()  # Close the window after success
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate shopping list: {e}")
        finally:
            conn.close()

    # Create a new window for selecting the meal plan
    select_meal_plan_window = tk.Toplevel(root)
    select_meal_plan_window.title("Select Meal Plan")
    select_meal_plan_window.geometry("400x200")

    tk.Label(select_meal_plan_window, text="Select a Meal Plan:").pack(pady=10)

    # Fetch all meal plan titles from the database
    conn = sqlite3.connect('recipe_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM meal_plans')
    meal_plan_titles = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Dropdown menu for selecting a meal plan
    selected_meal_plan = tk.StringVar(select_meal_plan_window)
    selected_meal_plan.set(meal_plan_titles[0] if meal_plan_titles else "No Meal Plans Available")
    meal_plan_dropdown = tk.OptionMenu(select_meal_plan_window, selected_meal_plan, *meal_plan_titles)
    meal_plan_dropdown.pack(pady=10)

    # Button to generate the shopping list
    tk.Button(select_meal_plan_window, text="Generate Shopping List", command=lambda: save_shopping_list(selected_meal_plan.get())).pack(pady=10)
