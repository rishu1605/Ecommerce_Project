import streamlit as st
import cloudinary
import cloudinary.uploader

# Configuration for Cloudinary
# For Unsigned uploads, we mainly need the Cloud Name
try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        secure = True
    )
except:
    # Manual fallback for test.py
    cloudinary.config(cloud_name="your_cloud_name", secure=True)

def upload_image_to_cloud(image_file):
    """Performs an UNSIGNED upload using your 'ml_default' preset."""
    try:
        # We use unsigned_upload and specify the preset name
        response = cloudinary.uploader.unsigned_upload(
            image_file, 
            upload_preset="ml_default", # Ensure this matches your Cloudinary dashboard
            folder="sic_mart_products"
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Unsigned Upload Error: {e}")
        return None