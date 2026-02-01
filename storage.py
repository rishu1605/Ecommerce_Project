import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_products():
    file_path = "data.csv" # <--- MAKE SURE THIS MATCHES YOUR FILE NAME EXACTLY
    
    # Debug: Check if file exists
    if not os.path.exists(file_path):
        st.error(f"❌ File not found: {file_path}")
        return []

    try:
        df = pd.read_csv(file_path)
        
        # Debug: Check if CSV is empty
        if df.empty:
            st.warning("⚠️ The CSV file is empty!")
            return []

        products = []
        for i, row in df.iterrows():
            # Use .get() to avoid crashes if a column is missing
            products.append({
                "id": i,
                "name": row.get('product_name', 'No Name'),
                "category": row.get('category', 'General'),
                "price": row.get('price', 0),
                "mfr": row.get('manufacturer', 'Unknown'),
                "description": row.get('description', ''),
                "model": row.get('model', 'N/A'),
                "year": row.get('year', 2024),
                "specs": row.get('specs', ''),
                "image": row.get('image_url', 'https://picsum.photos/200')
            })
        return products

    except Exception as e:
        st.error(f"🔥 Script Error: {e}")
        return []