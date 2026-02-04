import streamlit as st
from .auth_backend import login_admin

def render_admin_auth():
    # Centered layout for a login-gate feel
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #FFD700;'>🛡️ ADMIN TERMINAL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #87CEEB;'>SIC MART MASTER CONTROL</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.form("admin_gate"):
            adm_id = st.text_input("Administrator ID")
            adm_pwd = st.text_input("Security Key", type="password")
            
            # Form Submit
            if st.form_submit_button("UNSEAL ACCESS", use_container_width=True):
                user, msg = login_admin(adm_id, adm_pwd)
                
                if user:
                    st.session_state.user_data = user
                    st.session_state.role = "admin"
                    st.session_state.admin_nav = "📊 Analytics" # Land on Analytics first
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        
        st.caption("⚠️ Unauthorized access attempts are logged and reported.")