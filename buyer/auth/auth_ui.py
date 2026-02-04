import streamlit as st
from .auth_backend import handle_buyer_login, handle_buyer_registration

def render_buyer_auth():
    """
    Displays the Buyer Login and Registration.
    """
    st.markdown("<h2 style='text-align: center;'>🛍️ SIC Mart Buyer Portal</h2>", unsafe_allow_html=True)
    
    # We define these as tabs so they don't overlap
    tab_login, tab_reg = st.tabs(["Customer Login", "Join SIC Mart"])

    with tab_login:
        with st.form("buyer_login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if email and password:
                    handle_buyer_login(email, password)
                else:
                    st.warning("Please enter your credentials.")

    with tab_reg:
        with st.form("buyer_registration_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input("Create Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Create My Account", use_container_width=True):
                if password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif name and email:
                    handle_buyer_registration(name, email, password)
                else:
                    st.error("Please fill in all details.")