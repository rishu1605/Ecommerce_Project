import streamlit as st
import cloudinary
import cloudinary.uploader

# Configuration logic mapping to your specific secrets.toml keys
try:
    cloudinary.config(
        cloud_name = st.secrets["CLOUDINARY_NAME"],
        api_key = st.secrets["CLOUDINARY_KEY"],
        api_secret = st.secrets["CLOUDINARY_SECRET"],
        secure = True
    )
except Exception:
    # Manual Fallback using your verified credentials
    cloudinary.config(
        cloud_name = "drvwqubls",
        api_key = "875357953927593",
        api_secret = "3OV41fTxgjADdj-6Ln4N1Dbcljk",
        secure = True
    )

def upload_to_cloudinary(image_file):
    """Performs an UNSIGNED upload using the ml_default preset."""
    try:
        response = cloudinary.uploader.unsigned_upload(
            image_file, 
            upload_preset="ml_default", 
            folder="sic_mart_products"
        )
        return response.get("secure_url")
    except Exception as e:
        st.error(f"Cloudinary Error: {e}")
        return None