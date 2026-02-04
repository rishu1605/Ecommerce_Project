import streamlit as st
from common.image_utils import upload_image_to_cloud
import database as db

def render_inventory_mgmt():
    st.header("📦 Shop Inventory")
    seller_id = st.session_state.user_data['user_id']

    with st.expander("➕ Add New Product", expanded=True):
        with st.form("add_prod"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0.0)
            stock = st.number_input("Stock", min_value=1)
            img_file = st.file_uploader("Product Image", type=['jpg','png'])
            
            if st.form_submit_button("List Product"):
                if name and img_file:
                    url = upload_image_to_cloud(img_file)
                    if url:
                        db.execute_query(
                            "INSERT INTO products (seller_id, name, price, stock, image_url) VALUES (?,?,?,?,?)",
                            (seller_id, name, price, stock, url)
                        )
                        st.success("Product Live!")
                        st.rerun()