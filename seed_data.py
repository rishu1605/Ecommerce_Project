import sqlite3
import csv
import os

def seed_from_csv():
    db_path = 'ecommerce.db'
    csv_path = 'products.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found! Create the CSV file first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Create Tables First
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS sellers (id INTEGER PRIMARY KEY AUTOINCREMENT, store_name TEXT UNIQUE, balance REAL DEFAULT 0.0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, category TEXT, seller_id INTEGER, stock INTEGER, specs TEXT, images TEXT)')

    # 2. Setup SIC Seller
    cursor.execute("INSERT OR IGNORE INTO sellers (id, store_name, balance) VALUES (1, 'SIC', 0.0)")
    
    # 3. Read CSV and Insert
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute('''
                    INSERT OR REPLACE INTO products (id, name, category, price, stock, seller_id, specs, images)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['id'], row['name'], row['category'], row['price'], 
                    row['stock'], row['seller_id'], row['specs'], row['images']
                ))
        conn.commit()
        print("✅ Success! 60 products seeded without Pandas.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_from_csv()