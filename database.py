import sqlite3
import pandas as pd

DB_PATH = "sic_mart.db"

# -------------------- CONNECTION --------------------
def get_connection():
    return sqlite3.connect(DB_PATH)

# -------------------- TABLE SETUP --------------------
def set_up_tables():
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. USERS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT,
            address TEXT, -- Main profile address
            upi_id TEXT,
            bank_acc TEXT,
            ifsc TEXT,
            acc_holder TEXT,
            branch TEXT
        )
        """)

        # 2. ADDRESSES (NEW: Stores multiple addresses per user)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            label TEXT, -- e.g., 'Home', 'Office', 'Other'
            address_text TEXT NOT NULL,
            is_default INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)

        # 3. SELLER PROFILES
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS seller_profiles (
            seller_id INTEGER PRIMARY KEY,
            store_name TEXT,
            gst_number TEXT,
            pan_number TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (seller_id) REFERENCES users(user_id)
        )
        """)

        # 4. PRODUCTS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT,
            image_url TEXT,
            status TEXT DEFAULT 'active',
            is_approved INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users(user_id)
        )
        """)

        # 5. WALLETS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0.0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)

        # 6. TRANSACTIONS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            status TEXT,
            order_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)

        # 7. ORDERS (Updated to include shipping_address)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer_id INTEGER,
            seller_id INTEGER,
            product_name TEXT,
            amount REAL,
            shipping_address TEXT, -- Captured at checkout
            status TEXT DEFAULT 'Confirmed',
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (buyer_id) REFERENCES users(user_id),
            FOREIGN KEY (seller_id) REFERENCES users(user_id)
        )
        """)

        # 8. PAYMENTS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            user_id INTEGER,
            amount REAL,
            type TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)

        # 9. CART
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (buyer_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """)

        conn.commit()

# -------------------- QUERY HELPERS --------------------
def execute_query(query, params=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()

def fetch_query(query, params=None):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)

if __name__ == "__main__":
    set_up_tables()
    print("Database tables synchronized successfully!")