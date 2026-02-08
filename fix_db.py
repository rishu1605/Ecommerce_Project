import sqlite3

def migrate_orders_table():
    conn = sqlite3.connect("sic_mart.db")
    cursor = conn.cursor()
    
    try:
        # This command adds the missing column to your existing table
        cursor.execute("ALTER TABLE orders ADD COLUMN shipping_address TEXT")
        conn.commit()
        print("✅ Successfully added 'shipping_address' to orders table!")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ Column already exists.")
        else:
            print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_orders_table()