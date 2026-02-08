import streamlit as st
import database as db
import time
import pandas as pd
from buyer.cart.cart_backend import add_to_cart

def render_ads():
    """Renders a responsive, rotating advertisement banner."""
    images = [
        "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?q=80&w=2070&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=2070&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=2070&auto=format&fit=crop"
    ]
    ads_html = f"""
    <div style="width:100%; height:220px; overflow:hidden; border-radius:15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2);">
        <img id="slide" src="{images[0]}" style="width:100%; height:100%; object-fit:cover; transition: 0.8s ease-in-out;">
    </div>
    <script>
        var images = {images}; var index = 0;
        setInterval(function() {{
            index = (index + 1) % images.length;
            var imgElem = document.getElementById("slide");
            if(imgElem) imgElem.src = images[index];
        }}, 4000); 
    </script>
    """
    st.components.v1.html(ads_html, height=230)

def render_detailed_view():
    """Renders the single-product focus page with an interactive gallery."""
    product = st.session_state.get("selected_product_data")
    
    # Defensive check: if product data is missing, reset state and return
    if product is None:
        st.session_state.selected_product_id = None
        st.rerun()

    if st.button("⬅️ Back to Shop"):
        st.session_state.selected_product_id = None
        st.session_state.selected_product_data = None
        if "active_img_idx" in st.session_state:
            del st.session_state["active_img_idx"]
        st.rerun()

    # Image Gallery Logic
    img_url_str = str(product.get('image_url', ""))
    all_images = [url for url in img_url_str.split("|") if url and url.lower() != 'nan']
    
    if "active_img_idx" not in st.session_state:
        st.session_state.active_img_idx = 0

    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        # Main Display Image
        current_img = all_images[st.session_state.active_img_idx] if all_images else ""
        if current_img:
            st.markdown(f'''
                <div style="background-color: white; padding: 10px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 15px; text-align:center;">
                    <img src="{current_img}" style="width: 100%; border-radius: 10px; object-fit: contain; max-height: 450px;">
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.info("No image available for this product.")
        
        # Thumbnail selection
        if len(all_images) > 1:
            st.write("🔍 **View Gallery**")
            t_cols = st.columns(min(len(all_images), 6))
            for idx, img_url in enumerate(all_images):
                with t_cols[idx % 6]:
                    is_active = st.session_state.active_img_idx == idx
                    border = "3px solid #2563eb" if is_active else "1px solid #ddd"
                    st.markdown(f'''
                        <div style="border: {border}; border-radius: 8px; overflow: hidden; height: 60px;">
                            <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                    ''', unsafe_allow_html=True)
                    if st.button("View", key=f"sel_img_{idx}", use_container_width=True):
                        st.session_state.active_img_idx = idx
                        st.rerun()
    
    with col2:
        st.markdown(f"<h1 style='margin-bottom:0;'>{product['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: gray; font-size: 0.9rem;'>Category: {product['category']}</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:#2563eb; font-weight:800;'>₹{product['price']:,}</h2>", unsafe_allow_html=True)
        st.write("---")
        
        st.markdown("### Product Description")
        st.write(product.get('description', "No description provided."))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🛒 Add to Cart", key="detail_add_btn", use_container_width=True, type="primary"):
                user_id = st.session_state.user_data.get('user_id')
                if user_id:
                    add_to_cart(product['product_id'], user_id)
                    st.toast(f"Added {product['name']} to cart!") 
                else:
                    st.error("Please log in to add items.")
        with c2:
            if st.button("⚡ Buy Now", use_container_width=True, key="detail_buy_now"):
                st.session_state.buy_now_active = True
                st.session_state.buy_now_item = product
                st.rerun()

def render_marketplace():
    """Renders the main Marketplace UI with search, categories, and product grid."""
    # Centralized Styling
    st.markdown("""
        <style>
        .logo-text {
            font-size: 2.8rem; font-weight: 850;
            background: linear-gradient(to right, #2563eb, #7c3aed);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            letter-spacing: -1.5px; line-height: 1.2;
        }
        .trust-bar {
            background: rgba(37, 99, 235, 0.05); border-radius: 12px;
            padding: 15px; margin: 20px 0; display: flex;
            justify-content: space-around; border: 1px solid rgba(37, 99, 235, 0.1);
        }
        .trust-item { font-weight: 600; font-size: 0.85rem; }
        
        /* Category button styling */
        div.stButton > button[key^="cat_btn_"] {
            border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 12px;
            height: 90px; font-weight: 700; background-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    # Check for Routing to Detail View
    if st.session_state.get("selected_product_id"):
        render_detailed_view()
        return

    # Header Section
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; padding: 10px 0 25px 0;">
            <div style="font-size: 55px;">🛒</div>
            <div>
                <div class="logo-text">SIC Mart</div>
                <div style="color: gray; font-weight: 500; font-size: 1rem;">
                    Smart • Instant • Choice • Premium Marketplace
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Fetch Category Data
    categories_df = db.fetch_query("SELECT DISTINCT category FROM products")
    cat_list = ["All Categories"] + (categories_df['category'].tolist() if categories_df is not None and not categories_df.empty else [])
    
    # Handle category routing from buttons
    default_cat_index = 0
    if "forced_category" in st.session_state:
        try:
            default_cat_index = cat_list.index(st.session_state.forced_category)
            del st.session_state["forced_category"]
        except (ValueError, IndexError):
            default_cat_index = 0

    # User Welcome and Search
    user_name = st.session_state.get('user_data', {}).get('name', 'Shopper')
    st.markdown(f"#### 👋 Welcome back, {user_name}!")

    col_search, col_cat = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Search", placeholder="What are you looking for today?", label_visibility="collapsed")
    with col_cat:
        selected_category = st.selectbox("Category", options=cat_list, index=default_cat_index, label_visibility="collapsed")

    render_ads()

    st.markdown("""
        <div class="trust-bar">
            <div class="trust-item">🚀 Fast Delivery</div>
            <div class="trust-item">🛡️ Secure Payments</div>
            <div class="trust-item">🔄 Easy Returns</div>
            <div class="trust-item">⭐ 100% Authentic</div>
        </div>
    """, unsafe_allow_html=True)

    # Browse by Category Icons
    st.subheader("Browse by Category")
    top_cats = cat_list[1:7]  # Get up to 6 real categories
    cat_icons = ["📱", "👕", "🧸", "🏠", "📚", "⚽"] 
    c_cols = st.columns(6)
    
    for idx, cat in enumerate(top_cats):
        with c_cols[idx]:
            icon = cat_icons[idx] if idx < len(cat_icons) else "🛍️"
            if st.button(f"{icon}\n\n{cat}", key=f"cat_btn_{idx}", use_container_width=True):
                st.session_state.forced_category = cat
                st.rerun()

    st.write("---")
    st.subheader("✨ Featured Products")
    
    # Product Grid Fetch and Filter
    products_df = db.fetch_query("SELECT * FROM products")
    if products_df is not None and not products_df.empty:
        # Local Filtering Logic
        filtered_df = products_df.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False, na=False)]
        if selected_category != "All Categories":
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
        if filtered_df.empty:
            st.info("No products found matching your criteria.")
        else:
            # Display Grid (3 items per row)
            for i in range(0, len(filtered_df), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(filtered_df):
                        row = filtered_df.iloc[i + j]
                        with cols[j]:
                            with st.container(border=True):
                                # First image as thumbnail
                                img_str = str(row.get('image_url', ""))
                                img = img_str.split("|")[0] if img_str and img_str.lower() != 'nan' else ""
                                
                                st.markdown(f'''
                                    <div style="height:180px; display:flex; align-items:center; justify-content:center; overflow:hidden; margin-bottom:15px; background-color:#f8fafc; border-radius:8px;">
                                        <img src="{img}" style="max-height:100%; max-width:100%; object-fit:contain;">
                                    </div>
                                ''', unsafe_allow_html=True)
                                
                                st.markdown(f'<div style="height:45px; overflow:hidden; font-weight:700; line-height:1.2; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">{row["name"]}</div>', unsafe_allow_html=True)
                                st.markdown(f"<div style='color:#2563eb; font-weight:800; font-size:1.2rem; margin: 10px 0;'>₹{row['price']:,}</div>", unsafe_allow_html=True)
                                
                                b1, b2 = st.columns(2)
                                with b1:
                                    if st.button("View", key=f"v_{row['product_id']}", use_container_width=True):
                                        st.session_state.selected_product_id = row['product_id']
                                        st.session_state.selected_product_data = row
                                        st.rerun()
                                with b2:
                                    if st.button("🛒 Add", key=f"a_{row['product_id']}", use_container_width=True, type="primary"):
                                        uid = st.session_state.user_data.get('user_id')
                                        if uid:
                                            add_to_cart(row['product_id'], uid)
                                            st.toast(f"Added to cart!")
                                            time.sleep(2)
                                            st.rerun()
                                        else:
                                            st.error("Please login first.")
    else:
        st.warning("The marketplace is currently empty.")