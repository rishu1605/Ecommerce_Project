import streamlit as st
from .home_backend import get_marketplace_products
# Import the backend function that talks to the database
from buyer.cart.cart_backend import add_to_cart

def render_marketplace():
    st.title("🛒 SIC Mart Marketplace")
    
    # 1. Search Bar Logic
    search_query = st.text_input("🔍 Search products...", placeholder="Enter product name, category, or keywords")
    st.markdown("---")

    # 2. Fetch products
    products = get_marketplace_products(search_query if search_query else None)

    if products is None or products.empty:
        st.info("No products available at the moment. Try a different search or check back later!")
    else:
        # 3. Grid Layout
        cols = st.columns(3)
        for index, row in products.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    # --- IMAGE HANDLING ---
                    raw_urls = row.get('image_url', "")
                    url_list = raw_urls.split("|") if raw_urls else []
                    main_image = url_list[0] if url_list else "https://via.placeholder.com/300?text=No+Image"
                    
                    st.image(main_image, use_container_width=True)
                    
                    # --- PRODUCT DETAILS ---
                    st.subheader(row['name'])
                    st.write(f"### ₹{row['price']:,}")
                    
                    st.caption(f"🏪 Store: {row['store_name']}")
                    st.markdown(f"🏷️ `{row['category']}`")
                    
                    desc = row.get('description', "No description available.")
                    st.write(desc[:80] + "..." if len(desc) > 80 else desc)
                    
                    # --- REFRESHED BUTTON LOGIC ---
                    if st.button(f"Add to Cart", key=f"btn_{row['product_id']}", use_container_width=True):
                        # Ensure user is logged in to get their ID
                        if "user_data" in st.session_state:
                            buyer_id = st.session_state.user_data['user_id']
                            
                            # Call the database-linked function
                            add_to_cart(row['product_id'], buyer_id)
                            
                            st.toast(f"✅ {row['name']} added to cart!", icon="🛒")
                        else:
                            st.error("Please log in to add items to your cart.")