import sqlite3

def view_database_entries():
    # Connect to the database file you created
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    print("--- REGISTERED BUYERS (Users Table) ---")
    try:
        # Selecting columns defined in database.py: id, name, username, email
        cursor.execute("SELECT id, name, username, email FROM users")
        buyers = cursor.fetchall()
        
        if not buyers:
            print("No buyers found.")
        for row in buyers:
            print(f"ID: {row[0]} | Name: {row[1]} | Username: {row[2]} | Email: {row[3]}")
    except sqlite3.OperationalError:
        print("Users table does not exist yet.")

    print("\n--- REGISTERED SELLERS (Sellers Table) ---")
    try:
        # Selecting columns defined in database.py: id, store_name
        cursor.execute("SELECT id, store_name FROM sellers")
        sellers = cursor.fetchall()
        
        if not sellers:
            print("No sellers found.")
        for row in sellers:
            print(f"ID: {row[0]} | Store Name: {row[1]}")
    except sqlite3.OperationalError:
        print("Sellers table does not exist yet.")

    conn.close()

if __name__ == "__main__":
    view_database_entries()