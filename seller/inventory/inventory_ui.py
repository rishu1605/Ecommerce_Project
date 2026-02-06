import streamlit as st
import sqlite3
import database as db
from common.image_utils import upload_to_cloudinary

def show_inventory_listing():
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
                    st.error("Upload failed. Ensure 'ml_default' is set to Unsigned in Cloudinary.")
                    return

                # 2. Database Preparation
                image_url_string = "|".join(urls)
                seller_id = st.session_state.user_data.get('user_id')
                
                if not seller_id:
                    st.error("Session error: Seller ID not found. Please log in again.")
                    return

                # 3. Direct SQL Execution to see the ACTUAL error
                # Note: We use the exact order from your PRAGMA check
                conn = sqlite3.connect('sic_mart.db')
                cursor = conn.cursor()
                
                try:
                    cursor.execute("""
                        INSERT INTO products (seller_id, name, price, stock, description, category, image_url)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
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