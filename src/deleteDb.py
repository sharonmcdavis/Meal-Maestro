import sqlite3

def delete_all_tables():
    conn = sqlite3.connect('recipe_database.db')
    cursor = conn.cursor()
    
    # Drop all tables
    cursor.execute('DROP TABLE IF EXISTS recipes')
    cursor.execute('DROP TABLE IF EXISTS meal_plans')
    cursor.execute('DROP TABLE IF EXISTS shopping_lists')
    
    conn.commit()
    conn.close()
    print("All tables deleted.")

if __name__ == "__main__":
    delete_all_tables()