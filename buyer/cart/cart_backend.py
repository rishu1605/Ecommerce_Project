import streamlit as st

def add_to_cart(product):
    """Adds a product object to the session-based cart."""
    if "cart" not in st.session_state:
        st.session_state.cart = []
    
    # Check if item already exists to increment quantity
    for item in st.session_state.cart:
        if item['id'] == product['id']:
            item['quantity'] += 1
            return
            
    product['quantity'] = 1
    st.session_state.cart.append(product)

def get_cart_total():
    """Calculates total price of items in cart."""
    if "cart" not in st.session_state: return 0
    return sum(item['price'] * item['quantity'] for item in st.session_state.cart)