import streamlit as st
import sqlite3
import time
import database as db
from common.image_utils import upload_to_cloudinary

def ensure_db_schema():
    """Checks and adds missing columns to the products table if they don't exist."""
    conn = sqlite3.connect('sic_mart.db')
    cursor = conn.cursor()
    try:
        # Check for 'status' column
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'status' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN status TEXT DEFAULT 'active'")
        if 'is_approved' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN is_approved INTEGER DEFAULT 1")
        
        conn.commit()
    except Exception as e:
        st.error(f"Schema Update Error: {e}")
    finally:
        conn.close()

def show_inventory_listing():
    """Handles the creation of new product listings with Cloudinary integration."""
    # Run schema check before showing the form
    ensure_db_schema()
    
    st.markdown("### 🏺 List New Premium Item")
    
    with st.form("seller_listing_form", clear_on_submit=True):
        name = st.text_input("Product Name", placeholder="e.g. Rolex Submariner 2024")
        
        col_cat, col_price, col_stock = st.columns([2, 1, 1])
        with col_cat:
            category = st.selectbox("Category", ["Sports", "Clothing", "Grocery", "Jwellery", "Electronics", "Utility"])
        with col_price:
            price = st.number_input("Price (₹)", min_value=0.0, format="%.2f")
        with col_stock:
            stock = st.number_input("Stock", min_value=1, step=1)

        description = st.text_area("Product Specifications & Details", height=150)
        uploaded_files = st.file_uploader("Upload Images (3-10)", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True)

        submit_btn = st.form_submit_button("💎 Finalize & List Item", use_container_width=True)

        if submit_btn:
            if not name or not description:
                st.error("Please provide both a name and description.")
                return

            if len(uploaded_files) < 3:
                st.warning(f"Standard Requirement: At least 3 images needed. (Current: {len(uploaded_files)})")
                return

            try:
                # 1. Image Upload (Unsigned Mode)
                urls = []
                with st.spinner("Uploading to Cloudinary..."):
                    for file in uploaded_files:
                        url = upload_to_cloudinary(file) 
                        if url:
                            urls.append(url)
                
                if len(urls) < 3:
                    st.error("Upload failed. Ensure Cloudinary settings are correct.")
                    return

                # 2. Database Preparation
                image_url_string = "|".join(urls)
                seller_id = st.session_state.user_data.get('id') or st.session_state.user_data.get('user_id')
                
                if not seller_id:
                    st.error("Session error: Seller ID not found. Please log in again.")
                    return

                # 3. SQL Execution
                conn = sqlite3.connect('sic_mart.db')
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO products (seller_id, name, price, stock, description, category, image_url, status, is_approved)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'active', 1)
                    """, (seller_id, name, price, stock, description, category, image_url_string))
                    
                    conn.commit()
                    st.balloons()
                    st.success(f"Successfully listed '{name}'!")
                except sqlite3.Error as sql_e:
                    st.error(f"SQL Error: {sql_e}")
                finally:
                    conn.close()
            except Exception as e:
                st.error(f"General Error: {e}")

def render_inventory_management():
    """Allows sellers to modify or delete their products."""
    st.markdown("### 🛠️ Manage Existing Inventory")
    seller_id = st.session_state.user_data.get('id') or st.session_state.user_data.get('user_id')
    
    # Fetch current inventory
    query = "SELECT product_id, name, price, stock, category FROM products WHERE seller_id = ?"
    products = db.fetch_query(query, (seller_id,))

    if products.empty:
        st.info("You currently have no items in your inventory.")
        return

    for _, row in products.iterrows():
        with st.expander(f"📦 {row['name']} (ID: {row['product_id']})"):
            # Update Form
            with st.form(key=f"edit_form_{row['product_id']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_price = st.number_input("Update Price (₹)", value=float(row['price']), min_value=0.0, key=f"p_{row['product_id']}")
                with col2:
                    new_stock = st.number_input("Update Stock", value=int(row['stock']), min_value=0, key=f"s_{row['product_id']}")
                with col3:
                    cat_list = ["Sports", "Clothing", "Grocery", "Jwellery", "Electronics", "Utility"]
                    current_cat_idx = cat_list.index(row['category']) if row['category'] in cat_list else 0
                    new_cat = st.selectbox("Category", cat_list, index=current_cat_idx, key=f"c_{row['product_id']}")

                if st.form_submit_button("✅ Save Changes", use_container_width=True):
                    db.execute_query(
                        "UPDATE products SET price=?, stock=?, category=? WHERE product_id=?",
                        (new_price, new_stock, new_cat, row['product_id'])
                    )
                    st.success("Product updated successfully!")
                    st.balloons
                    time.sleep(2)
                    st.rerun()
            
            # Delete Button
            if st.button(f"🗑️ Delete {row['name']}", key=f"del_{row['product_id']}", use_container_width=True):
                db.execute_query("DELETE FROM products WHERE product_id=?", (row['product_id'],))
                st.warning(f"Item {row['product_id']} removed from inventory.")
                time.sleep(2)
                st.rerun()