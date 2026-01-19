import streamlit as st

def add_to_cart(product):
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    # Adding the full dictionary to keep image and tech specs accessible in the cart
    st.session_state.cart.append(product)
    st.toast(f"✅ {product['name']} added to cart!")

def remove_from_cart(index):
    if 'cart' in st.session_state:
        st.session_state.cart.pop(index)
        st.rerun()

def calculate_total():
    if 'cart' not in st.session_state or not st.session_state.cart:
        return 0
    return sum(item['price'] for item in st.session_state.cart)

def save_complaint(name, product, issue):
    if 'complaints' not in st.session_state:
        st.session_state.complaints = []
    st.session_state.complaints.append({
        "User": name, 
        "Product": product, 
        "Issue": issue
    })
    return True