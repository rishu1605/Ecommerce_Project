import streamlit as st
from buyer.auth.auth_backend import authenticate_user, register_user, verify_email_exists, reset_password

def render_buyer_auth():
    st.markdown("""
        <style>
        .login-card {
            background: white; padding: 1.5rem; border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center;
        }
        div[data-baseweb="input"] {
            border: 2px solid #e2e8f0 !important; border-radius: 10px !important;
        }
        /* Style for the Forgot Password link */
        .forgot-btn {
            color: #2563eb; font-size: 0.85rem; font-weight: 600;
            text-decoration: none; cursor: pointer; float: right; margin-top: -15px;
        }
        </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="login-card"><h1 style="color:#2563eb; margin:0;">SIC Mart</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔒 Login", "✨ Register"])
        
        with tab1:
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            
            # --- FORGOT PASSWORD FEATURE ---
            if st.button("Forgot Password?", type="secondary", help="Click to reset your password"):
                show_reset_modal()

            if st.button("Sign In", use_container_width=True, type="primary"):
                user = authenticate_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user
                    st.session_state.role = "buyer"
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with tab2:
            # (Keep your existing registration code here)
            name = st.text_input("Full Name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            if st.button("Create Account", use_container_width=True):
                success, msg = register_user(name, reg_email, reg_pass)
                if success: st.success(msg)
                else: st.error(msg)

@st.dialog("Reset Password")
def show_reset_modal():
    st.write("Enter your registered email to reset your password.")
    res_email = st.text_input("Registered Email")
    if st.button("Verify Email"):
        if verify_email_exists(res_email):
            st.session_state.allow_reset = res_email
            st.success("Email verified! Enter your new password below.")
        else:
            st.error("Email not found in our system.")
    
    if st.session_state.get("allow_reset"):
        new_p = st.text_input("New Password", type="password")
        if st.button("Update Password"):
            success, msg = reset_password(st.session_state.allow_reset, new_p)
            if success:
                st.success(msg)
                st.session_state.allow_reset = None # Clear state
            else:
                st.error(msg)