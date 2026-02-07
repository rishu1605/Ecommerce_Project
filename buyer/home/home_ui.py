import streamlit as st
from .home_backend import get_marketplace_products
from buyer.cart.cart_backend import add_to_cart

def render_marketplace():
    # --- 1. GLOBAL STYLING & ANIMATIONS ---
    st.markdown("""
        <style>
        /* Smooth fade-in for product details */
        .main-img-container {
            animation: fadeIn 0.5s;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        /* Custom Button Styling */
        .stButton>button {
            border-radius: 8px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            border-color: #007BFF;
            color: #007BFF;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navigation Logic
    if "selected_product_id" in st.session_state and st.session_state.selected_product_id:
        render_detailed_view()
        return

    st.title("🛒 SIC Mart Marketplace")
    
    # Search Bar
    search_query = st.text_input("🔍 Search products...", placeholder="Enter product name, category, or keywords")
    st.markdown("---")

    # Fetch products
    products = get_marketplace_products(search_query if search_query else None)

    if products is None or products.empty:
        st.info("No products available at the moment.")
    else:
        # --- 2. GRID LAYOUT ---
        cols = st.columns(3)
        for index, row in products.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    url_list = row.get('image_url', "").split("|") if row.get('image_url') else []
                    main_image = url_list[0] if url_list else "https://via.placeholder.com/300"
                    
                    st.image(main_image, use_container_width=True)
                    st.subheader(row['name'])
                    st.write(f"### ₹{row['price']:,}")
                    st.caption(f"🏪 {row['store_name']}")

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🔍 View", key=f"view_{row['product_id']}", use_container_width=True):
                            st.session_state.selected_product_id = row['product_id']
                            st.session_state.selected_product_data = row
                            st.session_state.gallery_idx = 0 
                            st.rerun()
                    with c2:
                        if st.button("🛒 Add", key=f"btn_{row['product_id']}", use_container_width=True):
                            handle_cart_action(row)

def render_detailed_view():
    """Renders detailed page with smooth image sliding & filmstrip navigation."""
    product = st.session_state.selected_product_data
    urls = product['image_url'].split("|") if product['image_url'] else []
    
    if st.button("⬅️ Back to Marketplace"):
        st.session_state.selected_product_id = None
        st.session_state.gallery_idx = 0
        st.rerun()

    st.markdown("---")
    col1, col2 = st.columns([1.5, 1])

    with col1:
        if urls:
            if "gallery_idx" not in st.session_state:
                st.session_state.gallery_idx = 0
            
            # --- MAIN IMAGE (Animated) ---
            st.markdown('<div class="main-img-container">', unsafe_allow_html=True)
            st.image(urls[st.session_state.gallery_idx], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # --- SLIDER CONTROLS ---
            c_prev, c_count, c_next = st.columns([1, 2, 1])
            with c_prev:
                if st.button("◀️ Previous", use_container_width=True):
                    st.session_state.gallery_idx = (st.session_state.gallery_idx - 1) % len(urls)
                    st.rerun()
            with c_count:
                # Progress indicator bar for smooth visual flow
                progress = (st.session_state.gallery_idx + 1) / len(urls)
                st.progress(progress)
                st.markdown(f"<p style='text-align:center'><b>Image {st.session_state.gallery_idx + 1} of {len(urls)}</b></p>", unsafe_allow_html=True)
            with c_next:
                if st.button("Next ▶️", use_container_width=True):
                    st.session_state.gallery_idx = (st.session_state.gallery_idx + 1) % len(urls)
                    st.rerun()
            
            # --- FILMSTRIP NAVIGATION ---
            st.write("Browse Gallery:")
            # Use dynamic columns to create a horizontal filmstrip
            num_thumbs = min(len(urls), 8)
            t_cols = st.columns(num_thumbs)
            for i in range(num_thumbs):
                with t_cols[i]:
                    # Using icons to indicate current position
                    is_active = i == st.session_state.gallery_idx
                    label = f"🔵" if is_active else f"⚪"
                    if st.button(label, key=f"thumb_{i}", use_container_width=True):
                        st.session_state.gallery_idx = i
                        st.rerun()
        else:
            st.image("https://via.placeholder.com/600?text=No+Images", use_container_width=True)

    with col2:
        # --- PRODUCT INFO ---
        st.title(product['name'])
        st.write(f"## ₹{product['price']:,}")
        st.markdown(f"**Seller:** {product['store_name']} | **Category:** {product['category']}")
        st.info(f"**Description:** \n\n {product.get('description', 'No specifications provided.')}")
        st.markdown("---")

        # --- ACTION BUTTONS ---
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🛒 Add to Cart", key="det_add", use_container_width=True):
                handle_cart_action(product)
        with b2:
            if st.button("⚡ Buy Now", key="det_buy", type="primary", use_container_width=True):
                handle_cart_action(product, redirect_to_cart=True)

def handle_cart_action(row, redirect_to_cart=False):
    """Encapsulates DB sync and instant session state updates."""
    if "user_data" not in st.session_state:
        st.error("Please log in to add items to your cart.")
        return

    buyer_id = st.session_state.user_data['user_id']
    
    try:
        # 1. Database Persistence
        add_to_cart(row['product_id'], buyer_id)
        
        # 2. Local Session Update (Makes it visible in Cart UI instantly)
        if 'cart' not in st.session_state:
            st.session_state.cart = []
        
        # Add entry if not already in session (to avoid visual duplicates)
        if not any(item['id'] == row['product_id'] for item in st.session_state.cart):
            st.session_state.cart.append({
                'id': row['product_id'],
                'name': row['name'],
                'price': row['price'],
                'seller_id': row['seller_id'],
                'image': row.get('image_url', "").split("|")[0] if row.get('image_url') else ""
            })

        st.toast(f"✅ {row['name']} added!", icon="🛒")
        
        if redirect_to_cart:
            st.session_state.current_page = "Cart" 
            st.rerun()
            
    except Exception as e:
        st.error(f"Failed to update cart: {e}")