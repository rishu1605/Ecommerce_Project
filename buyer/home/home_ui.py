import streamlit as st
from .home_backend import get_marketplace_products

def render_marketplace():
    st.title("🛒 SIC Mart Marketplace")
    
    # Add a Search Bar to trigger the search logic
    search_query = st.text_input("🔍 Search products...", placeholder="Enter product name, category, or keywords")
    st.markdown("---")

    # Fetch products using the backend logic
    products = get_marketplace_products(search_query if search_query else None)

    if products is None or products.empty:
        st.info("No products available at the moment. Try a different search or check back later!")
    else:
        # Create a grid layout for products
        cols = st.columns(3)
        for index, row in products.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    # --- IMAGE HANDLING ---
                    # Split the image_url string and take the first one
                    raw_urls = row.get('image_url', "")
                    url_list = raw_urls.split("|") if raw_urls else []
                    main_image = url_list[0] if url_list else "https://via.placeholder.com/300?text=No+Image"
                    
                    st.image(main_image, use_container_width=True)
                    # ----------------------

                    st.subheader(row['name'])
                    st.write(f"### ₹{row['price']:,}")
                    
                    # Store Name and Category
                    st.caption(f"🏪 Store: {row['store_name']}")
                    st.markdown(f"🏷️ `{row['category']}`")
                    
                    # Description snippet
                    desc = row['description']
                    st.write(desc[:80] + "..." if len(desc) > 80 else desc)
                    
                    if st.button(f"Add to Cart", key=f"btn_{row['product_id']}", use_container_width=True):
                        add_to_cart_logic(row)

def add_to_cart_logic(product):
    """Initializes cart in session and adds item."""
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    st.session_state.cart.append({
        'id': product['product_id'],
        'name': product['name'],
        'price': product['price'],
        'seller_id': product['seller_id']
    })
    st.toast(f"✅ {product['name']} added to cart!", icon="🛒")