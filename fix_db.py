import sqlite3

def patch_database():
    conn = sqlite3.connect('sic_mart.db')
    cursor = conn.cursor()
    
    # List of columns to check/add
    columns_to_add = [
        ("status", "TEXT DEFAULT 'active'"),
        ("is_approved", "INTEGER DEFAULT 1")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE products ADD COLUMN {col_name} {col_type}")
            print(f"✅ Added column: {col_name}")
        except sqlite3.OperationalError:
            print(f"ℹ️ Column {col_name} already exists.")
            
    conn.commit()
    conn.close()
    print("🚀 Database is now ready for uploads.")

if __name__ == "__main__":
    patch_database()