import streamlit as st
import database as db
import os
from buyer.cart.cart_backend import add_to_cart

def render_marketplace():
    # Fetch products from database
    products_df = db.fetch_query("SELECT * FROM products")
    
    if products_df.empty:
        st.info("No products available.")
        return

    user_id = st.session_state.user_data['user_id']

    for index, row in products_df.iterrows():
        with st.container(border=True):
            col_img, col_info = st.columns([1, 2.5])
            
            with col_img:
                # Image Logic: Splits the string and checks for URL or Local Path
                raw_image_data = row.get('image_url', "")
                url_list = raw_image_data.split("|") if raw_image_data else []
                img_path = url_list[0] if url_list else None
                
                if img_path and str(img_path) != 'nan':
                    if str(img_path).startswith(('http://', 'https://')):
                        st.image(img_path, use_container_width=True)
                    elif os.path.exists(str(img_path)):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.warning("⚠️ Image Missing")
                else:
                    st.write("🖼️ No Image")

            with col_info:
                st.subheader(row['name'])
                st.write(f"**Price:** ₹{row['price']:,}")
                
                c1, c2 = st.columns(2)
                if c1.button("🛒 Add to Cart", key=f"atc_{row['product_id']}", use_container_width=True):
                    add_to_cart(row['product_id'], user_id)

                if c2.button("⚡ Buy Now", key=f"buy_{row['product_id']}", type="primary", use_container_width=True):
                    st.session_state.buy_now_item = {
                        "product_id": row['product_id'],
                        "name": row['name'],
                        "price": row['price'],
                        "image_url": row.get('image_url', ""),
                        "quantity": 1
                    }
                    st.session_state.buy_now_active = True
                    st.rerun()