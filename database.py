import sqlite3
import csv
import os
from datetime import datetime

DB_NAME = "ecommerce.db"
UPLOAD_DIR = "uploaded_images"

def connect_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS sellers (id INTEGER PRIMARY KEY AUTOINCREMENT, store_name TEXT UNIQUE, balance REAL DEFAULT 0.0)')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, price REAL, category TEXT, 
        seller_id INTEGER, stock INTEGER, 
        specs TEXT, images TEXT)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, buyer_id INTEGER, total REAL, date TEXT, status TEXT DEFAULT "Paid")')
    cursor.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, method TEXT, status TEXT DEFAULT "Held in Escrow")')
    conn.commit()
    conn.close()

def save_images_locally(files, product_name):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    paths = []
    for i, file in enumerate(files):
        ext = file.name.split('.')[-1]
        filename = f"{product_name.replace(' ', '_')}_{i}.{ext}"
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        paths.append(path)
    return "|".join(paths)

def process_payment(buyer_id, cart, total, method):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        for pid, item in cart.items():
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?", (item['qty'], pid, item['qty']))
            if cursor.rowcount == 0: raise Exception(f"Stock out for {item['name']}")
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO orders (buyer_id, total, date) VALUES (?, ?, ?)", (buyer_id, total, date))
        oid = cursor.lastrowid
        cursor.execute("INSERT INTO transactions (order_id, method) VALUES (?, ?)", (oid, method))
        conn.commit()
        return True, oid
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally: conn.close()

def export_csv(table):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    file = f"{table}_data.csv"
    with open(file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
        writer.writerows(rows)
    conn.close()
    return file