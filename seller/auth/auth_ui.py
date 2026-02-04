import streamlit as st
from .auth_backend import handle_seller_registration, handle_seller_login

def render_seller_auth():
    st.markdown("<h2 style='text-align: center;'>🏪 Seller Central</h2>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["Seller Login", "Register as Merchant"])

    with tab_login:
        with st.form("seller_login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Access Dashboard", use_container_width=True):
                handle_seller_login(email, password)

    with tab_reg:
        with st.form("seller_registration"):
            st.info("Note: Your account will require Admin approval after registration.")
            name = st.text_input("Full Name")
            email = st.text_input("Business Email")
            store_name = st.text_input("Store Name")
            gst_number = st.text_input("GST Number (15-digit)")
            pan_number = st.text_input("PAN Number")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Register Store", use_container_width=True):
                if password != confirm:
                    st.error("Passwords do not match.")
                elif len(gst_number) != 15:
                    st.error("Please enter a valid 15-digit GST number.")
                elif name and email and store_name:
                    handle_seller_registration(name, email, store_name, gst_number, pan_number, password)
                else:
                    st.error("All fields are required.")