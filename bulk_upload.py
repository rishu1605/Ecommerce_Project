import pandas as pd
import sqlite3
import database

def bulk_upload_products(csv_file):
    # 1. Connect and ensure a default seller exists
    conn = database.connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM sellers LIMIT 1")
    seller = cursor.fetchone()
    if not seller:
        print("Creating default seller 'AdminStore'...")
        cursor.execute("INSERT INTO sellers (store_name, password) VALUES (?, ?)", ("AdminStore", "admin123"))
        conn.commit()
        seller_id = cursor.lastrowid
    else:
        seller_id = seller[0]

    print(f"Reading {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
        
        # FIX: Using headers that exist in your product.csv
        # We check for 'name' and 'price' instead of 'product_name' and 'final_price'
        df = df.dropna(subset=['name', 'price'])
        
        count = 0
        for _, row in df.iterrows():
            try:
                # MAPPING: Linking CSV columns to Database variables
                p_name = str(row['name']).strip()
                p_price = float(row['price']) 
                p_cat = str(row['category']).strip() if pd.notna(row['category']) else "General"
                p_img = str(row['image']).strip() if pd.notna(row['image']) else ""

                # Insert into products table (matches database.py schema)
                cursor.execute(
                    "INSERT INTO products (name, price, category, image_url, seller_id) VALUES (?, ?, ?, ?, ?)",
                    (p_name, p_price, p_cat, p_img, seller_id)
                )
                
                count += 1
                if count % 50 == 0:
                    conn.commit()
                    print(f"Uploaded {count} products...")
            
            except Exception as row_error:
                print(f"Skipping row: {row_error}")
                continue

        conn.commit()
        print(f"\n✅ Success! {count} products are now live in the database.")
        
    except Exception as e:
        print(f"❌ Major error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    database.create_tables()
    bulk_upload_products('product.csv')