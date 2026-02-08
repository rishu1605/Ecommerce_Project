import streamlit as st
import database as db
from buyer.cart.cart_backend import add_to_cart

def render_ads():
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
            document.getElementById("slide").src = images[index];
        }}, 4000); 
    </script>
    """
    st.components.v1.html(ads_html, height=230)

def render_detailed_view():
    product = st.session_state.get("selected_product_data")
    if product is None:
        st.session_state.selected_product_id = None
        st.rerun()

    if st.button("⬅️ Back to Shop"):
        st.session_state.selected_product_id = None
        st.session_state.selected_product_data = None
        st.rerun()

    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        img_url = str(product['image_url']).split("|")[0] if product['image_url'] else ""
        if img_url and img_url != 'nan':
            st.image(img_url, use_container_width=True)
    
    with col2:
        st.title(product['name'])
        st.subheader(f"Price: ₹{product['price']:,}")
        st.write("---")
        st.write(f"**Description:**\n\n{product['description']}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🛒 Add to Cart", key="detail_add_btn", use_container_width=True, type="primary"):
                user_id = st.session_state.user_data.get('user_id')
                add_to_cart(product['product_id'], user_id)
                st.rerun() 
        with c2:
            if st.button("⚡ Buy Now", use_container_width=True):
                st.session_state.buy_now_active = True
                st.session_state.buy_now_item = product
                st.rerun()

def render_marketplace():
    # --- 1. THEME-AWARE CSS STYLING ---
    st.markdown("""
        <style>
        .logo-text {
            font-size: 2.8rem; font-weight: 850;
            background: linear-gradient(to right, #2563eb, #7c3aed);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            letter-spacing: -1.5px; line-height: 1.2;
        }
        .cat-label { 
            text-align: center; font-size: 0.9rem; margin-top: 8px; 
            color: var(--text-color) !important; font-weight: 700 !important; 
        }
        .trust-bar {
            background: rgba(37, 99, 235, 0.1); border-radius: 12px;
            padding: 15px; margin: 20px 0; display: flex;
            justify-content: space-around; border: 1px solid rgba(37, 99, 235, 0.2);
        }
        .trust-item { color: var(--text-color) !important; font-weight: 600; font-size: 0.85rem; }
        h1, h2, h3, h4 { color: var(--text-color) !important; font-weight: 800 !important; }
        
        div.stButton > button[key^="cat_btn_"] {
            border: 1px solid rgba(128, 128, 128, 0.3); border-radius: 12px;
            height: 100px; font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.get("selected_product_id"):
        render_detailed_view()
        return

    # --- 2. HEADER ---
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; padding: 10px 0 25px 0;">
            <div style="font-size: 55px; filter: drop-shadow(0px 4px 10px rgba(37, 99, 235, 0.3));">🛒</div>
            <div>
                <div class="logo-text">SIC Mart</div>
                <div style="color: gray; font-weight: 500; font-size: 1rem;">
                    Smart • Instant • Choice • Premium Marketplace
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 3. DATA FETCHING ---
    categories_df = db.fetch_query("SELECT DISTINCT category FROM products")
    cat_list = ["All Categories"] + (categories_df['category'].tolist() if not categories_df.empty else [])
    
    default_cat_index = 0
    if "forced_category" in st.session_state:
        try:
            default_cat_index = cat_list.index(st.session_state.forced_category)
            del st.session_state["forced_category"]
        except ValueError:
            default_cat_index = 0

    # --- 4. SEARCH & FILTER ---
    user_data = st.session_state.get('user_data', {})
    user_name = user_data.get('name', 'Shopper')
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

    # --- 5. CATEGORY GRID ---
    st.subheader("Browse by Category")
    top_cats = categories_df['category'].tolist()[:6] if not categories_df.empty else []
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
    
    # --- 6. PRODUCT GRID LOGIC ---
    products_df = db.fetch_query("SELECT * FROM products")
    if products_df is not None and not products_df.empty:
        if search_query:
            products_df = products_df[products_df['name'].str.contains(search_query, case=False, na=False)]
        if selected_category != "All Categories":
            products_df = products_df[products_df['category'] == selected_category]
        
        if products_df.empty:
            st.info("No products found matching your criteria.")
        else:
            for i in range(0, len(products_df), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(products_df):
                        row = products_df.iloc[i + j]
                        with cols[j]:
                            with st.container(border=True):
                                img = str(row['image_url']).split("|")[0] if row['image_url'] else ""
                                st.markdown(f'''
                                    <div style="height:180px; display:flex; align-items:center; justify-content:center; overflow:hidden; margin-bottom:15px; background-color:#f8fafc; border-radius:8px;">
                                        <img src="{img}" style="max-height:100%; max-width:100%; object-fit:contain;">
                                    </div>
                                ''', unsafe_allow_html=True)
                                st.markdown(f'<div style="height:45px; overflow:hidden; font-weight:700; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">{row["name"]}</div>', unsafe_allow_html=True)
                                st.markdown(f"<div style='color:#2563eb; font-weight:800; font-size:1.2rem;'>₹{row['price']:,}</div>", unsafe_allow_html=True)
                                
                                b1, b2 = st.columns(2)
                                with b1:
                                    if st.button("View", key=f"d_{row['product_id']}", use_container_width=True):
                                        st.session_state.selected_product_id = row['product_id']
                                        st.session_state.selected_product_data = row
                                        st.rerun()
                                with b2:
                                    if st.button("🛒 Add", key=f"a_{row['product_id']}", use_container_width=True, type="primary"):
                                        # Safely get user_id from session
                                        uid = st.session_state.user_data.get('user_id')
                                        add_to_cart(row['product_id'], uid)
                                        # Success message is handled by st.toast inside backend, 
                                        # but rerun is needed to update the UI elsewhere
                                        st.rerun()
    else:
        st.warning("The marketplace is empty.")