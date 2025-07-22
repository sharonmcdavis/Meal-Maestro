import sqlite3

def check_table_info():
    conn = sqlite3.connect('mealMaestro_data.db')
    cursor = conn.cursor()

    # Check the schema of the meal_plans table
    cursor.execute("PRAGMA table_info(meal_plans)")
    columns = cursor.fetchall()

    if columns:
        print("meal_plans table exists. Columns:")
        for column in columns:
            print(column)
    else:
        print("meal_plans table does not exist.")

    conn.close()

if __name__ == "__main__":
    check_table_info()