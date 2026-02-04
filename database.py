import sqlite3
import pandas as pd

DB_PATH = 'sic_mart.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def set_up_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Users Table (Ensuring all profile fields exist)
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, 
            email TEXT UNIQUE, 
            password TEXT, 
            role TEXT,
            address TEXT,
            upi_id TEXT,
            bank_acc TEXT,
            ifsc TEXT,
            acc_holder TEXT,
            branch TEXT)''')

        # 2. Seller Profiles
        cursor.execute('''CREATE TABLE IF NOT EXISTS seller_profiles (
            seller_id INTEGER PRIMARY KEY, 
            store_name TEXT, 
            gst_number TEXT, 
            pan_number TEXT, 
            status TEXT DEFAULT 'Pending')''')

        # 3. Products
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            seller_id INTEGER,
            name TEXT, 
            price REAL, 
            stock INTEGER, 
            description TEXT, 
            category TEXT, 
            image_url TEXT)''')

        # 4. Wallets
        cursor.execute('''CREATE TABLE IF NOT EXISTS wallets (
            user_id INTEGER PRIMARY KEY, 
            balance REAL DEFAULT 0.0)''')
        
        # 5. Orders
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            buyer_id INTEGER,
            seller_id INTEGER, 
            product_name TEXT, 
            amount REAL, 
            status TEXT DEFAULT 'Confirmed', 
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        # 6. Payments
        cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            user_id INTEGER,
            amount REAL,
            type TEXT, 
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        conn.commit()
    
    # Run migrations to fix existing databases
    migrate_columns()

def migrate_columns():
    """Adds missing columns to the users table if they don't exist."""
    new_cols = [
        ('address', 'TEXT'),
        ('upi_id', 'TEXT'),
        ('bank_acc', 'TEXT'),
        ('ifsc', 'TEXT'),
        ('acc_holder', 'TEXT'),
        ('branch', 'TEXT')
    ]
    
    with get_connection() as conn:
        cursor = conn.cursor()
        # Get existing columns
        cursor.execute("PRAGMA table_info(users)")
        existing_cols = [col[1] for col in cursor.fetchall()]
        
        for col_name, col_type in new_cols:
            if col_name not in existing_cols:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                    print(f"Migration: Added column {col_name} to users table.")
                except Exception as e:
                    print(f"Migration Error on {col_name}: {e}")
        conn.commit()

def execute_query(query, params=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()

def fetch_query(query, params=None):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)