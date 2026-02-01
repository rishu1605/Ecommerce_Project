import streamlit as st

def add_to_cart(p_id, p_name, p_price, max_stock):
    """Adds or increments an item in the session-based cart."""
    if 'cart' not in st.session_state:
        st.session_state.cart = {}

    p_id = str(p_id) # Ensure ID is a string for dictionary keys
    
    # Check if we already have the item in cart
    current_qty = st.session_state.cart.get(p_id, {}).get('qty', 0)
    
    if current_qty < max_stock:
        if p_id in st.session_state.cart:
            st.session_state.cart[p_id]['qty'] += 1
        else:
            st.session_state.cart[p_id] = {
                'name': p_name,
                'price': p_price,
                'qty': 1
            }
        return True, f"Added {p_name} to cart!"
    else:
        return False, "Out of stock!"

def get_cart_total():
    """Calculates the total price of all items in the cart."""
    if 'cart' not in st.session_state:
        return 0.0
    return sum(item['price'] * item['qty'] for item in st.session_state.cart.values())

def remove_from_cart(p_id):
    """Removes an item or decreases quantity."""
    p_id = str(p_id)
    if 'cart' in st.session_state and p_id in st.session_state.cart:
        if st.session_state.cart[p_id]['qty'] > 1:
            st.session_state.cart[p_id]['qty'] -= 1
        else:
            del st.session_state.cart[p_id]