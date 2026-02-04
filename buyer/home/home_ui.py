import streamlit as st
import database as db

def render_marketplace():
    st.title("🛒 SIC Mart Marketplace")
    st.markdown("---")

    # Fetch products that have stock
    query = "SELECT * FROM products WHERE stock > 0"
    products = db.fetch_query(query)

    if products.empty:
        st.info("No products available at the moment. Check back later!")
    else:
        # Create a grid layout for products
        cols = st.columns(3)
        for index, row in products.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    st.subheader(row['name'])
                    st.write(f"**Price:** ₹{row['price']}")
                    st.write(f"**Category:** {row['category']}")
                    st.caption(row['description'])
                    
                    if st.button(f"Add to Cart", key=f"btn_{row['product_id']}"):
                        add_to_cart_logic(row)

def add_to_cart_logic(product):
    """Initializes cart in session and adds item."""
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # Check if item already in cart to increment quantity or just add
    st.session_state.cart.append({
        'id': product['product_id'],
        'name': product['name'],
        'price': product['price'],
        'seller_id': product['seller_id']
    })
    st.toast(f"✅ {product['name']} added to cart!")