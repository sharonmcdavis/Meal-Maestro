import sqlite3

def delete_all_tables():
    conn = sqlite3.connect('mealMaestro_data.db')
    cursor = conn.cursor()
    
    # Drop all tables
    cursor.execute('DROP TABLE IF EXISTS recipes')
    cursor.execute('DROP TABLE IF EXISTS ingredients')
    cursor.execute('DROP TABLE IF EXISTS meal_plans')
    cursor.execute('DROP TABLE IF EXISTS shopping_lists')
    cursor.execute('DROP TABLE IF EXISTS ingredient_dict')
    
    conn.commit()
    conn.close()
    print("All tables deleted.")

if __name__ == "__main__":
    delete_all_tables()