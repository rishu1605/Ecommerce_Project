import streamlit as st
import database as db
import os
from buyer.cart.cart_backend import add_to_cart

def render_marketplace():
    # --- 1. CUSTOM CSS BRANDING (SICMart Logo) ---
    st.markdown("""
        <style>
        .main-logo {
            font-family: 'Inter', Georgia, serif;
            font-weight: 800;
            font-size: 2.8rem;
            text-align: center;
            color: #FF5722;
            margin-top: -60px; /* Pushes text into the header space */
            margin-bottom: 10px;
            letter-spacing: -1.5px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        }
        /* Custom styling for the View Details button to make it pop */
        div.stButton > button:first-child {
            border-radius: 8px;
        }
        </style>
        <div class="main-logo">SICMart</div>
    """, unsafe_allow_html=True)

    # --- 2. DETAIL VIEW NAVIGATION ---
    if "selected_product_id" in st.session_state and st.session_state.selected_product_id:
        render_detailed_view()
        return

    st.title("🛒 SIC Mart Marketplace")

    # --- 3. FILTERS (Search & Category) ---
    col_search, col_cat = st.columns([2, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search", placeholder="Search by product name...", label_visibility="collapsed")
    
    with col_cat:
        # Fetch unique categories dynamically from your local SQLite database
        categories_df = db.fetch_query("SELECT DISTINCT category FROM products")
        if not categories_df.empty:
            cat_list = ["All Categories"] + categories_df['category'].tolist()
        else:
            cat_list = ["All Categories"]
        
        selected_category = st.selectbox("Category", options=cat_list, label_visibility="collapsed")

    st.markdown("---")

    # --- 4. FETCH & FILTER DATA ---
    products_df = db.fetch_query("SELECT * FROM products")
    
    if products_df is None or products_df.empty:
        st.info("No products found. Please ensure 'sic_mart.db' is in the project folder.")
        return

    # Apply Search Filter (Case-insensitive)
    if search_query:
        products_df = products_df[products_df['name'].str.contains(search_query, case=False, na=False)]

    # Apply Category Filter
    if selected_category != "All Categories":
        products_df = products_df[products_df['category'] == selected_category]

    if products_df.empty:
        st.warning("No products match your search or category selection.")
        return

    user_id = st.session_state.user_data['user_id']

    # --- 5. PRODUCT GRID (3 Columns) ---
    # Reset index so modulo positioning works after filtering
    products_df = products_df.reset_index(drop=True)
    
    cols = st.columns(3)
    for index, row in products_df.iterrows():
        with cols[index % 3]:
            with st.container(border=True):
                # --- Image Logic ---
                raw_image_data = row.get('image_url', "")
                url_list = str(raw_image_data).split("|") if raw_image_data else []
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

                # --- Info ---
                st.subheader(row['name'])
                st.write(f"**Price:** ₹{row['price']:,}")
                
                # --- Action Buttons ---
                if st.button("🔍 View Details", key=f"view_{row['product_id']}", use_container_width=True):
                    st.session_state.selected_product_id = row['product_id']
                    st.session_state.selected_product_data = row
                    st.session_state.gallery_idx = 0
                    st.rerun()

                if st.button("🛒 Add to Cart", key=f"atc_{row['product_id']}", use_container_width=True):
                    add_to_cart(row['product_id'], user_id)
                    st.toast(f"✅ {row['name']} added to cart!")

def render_detailed_view():
    """Shows one product in full detail with an image slider."""
    product = st.session_state.selected_product_data
    user_id = st.session_state.user_data['user_id']
    
    if st.button("⬅️ Back to Marketplace"):
        st.session_state.selected_product_id = None
        st.rerun()

    st.markdown("---")
    col_img, col_info = st.columns([1.5, 1])

    with col_img:
        # --- IMAGE SLIDER LOGIC ---
        urls = str(product['image_url']).split("|") if product['image_url'] else []
        if urls:
            if "gallery_idx" not in st.session_state:
                st.session_state.gallery_idx = 0
            
            st.image(urls[st.session_state.gallery_idx], use_container_width=True)
            
            if len(urls) > 1:
                c1, c2, c3 = st.columns([1, 2, 1])
                with c1:
                    if st.button("◀️ Prev"):
                        st.session_state.gallery_idx = (st.session_state.gallery_idx - 1) % len(urls)
                        st.rerun()
                with c2:
                    st.markdown(f"<p style='text-align:center'><b>{st.session_state.gallery_idx + 1} / {len(urls)}</b></p>", unsafe_allow_html=True)
                with c3:
                    if st.button("Next ▶️"):
                        st.session_state.gallery_idx = (st.session_state.gallery_idx + 1) % len(urls)
                        st.rerun()
        else:
            st.write("🖼️ No Images Available")

    with col_info:
        st.title(product['name'])
        st.write(f"## Price: ₹{product['price']:,}")
        st.write(f"**Category:** {product.get('category', 'N/A')}")
        st.markdown("---")
        st.write("**Product Description:**")
        st.write(product.get('description', "No detailed description provided."))

        if st.button("🛒 Add to Cart", key="det_atc", use_container_width=True):
            add_to_cart(product['product_id'], user_id)
            st.toast("Success! Added to cart.")

        if st.button("⚡ Buy Now", key="det_buy", type="primary", use_container_width=True):
            st.session_state.buy_now_item = {
                "product_id": product['product_id'],
                "name": product['name'],
                "price": product['price'],
                "image_url": product.get('image_url', ""),
                "quantity": 1
            }
            st.session_state.buy_now_active = True
            st.rerun()