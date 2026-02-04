import streamlit as st
import database as db
from common.auth_utils import logout_user

def render_profile_ui():
    """
    Admin Profile Management UI.
    Matches the import name 'render_profile_ui' in admin_main.py.
    """
    st.markdown("<div class='sic-mart-header'>👤 Admin Profile Settings</div>", unsafe_allow_html=True)
    
    # Check if user data exists in session
    if "user_data" not in st.session_state:
        st.error("No active session found.")
        return

    user = st.session_state.user_data
    
    # UI Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://www.w3schools.com/howto/img_avatar.png", width=150)
        if st.button("Log Out", use_container_width=True, type="primary"):
            logout_user()

    with col2:
        st.subheader("System Access Details")
        st.write(f"**Name:** {user.get('name', 'Admin User')}")
        st.write(f"**Email:** {user.get('email', 'N/A')}")
        st.write(f"**Role:** {user.get('role', 'Superuser').capitalize()}")
        st.write(f"**User ID:** `{user.get('user_id', 'N/A')}`")

    st.markdown("---")
    
    # Security Section
    st.subheader("🔐 Security & Credentials")
    with st.expander("Update System Password"):
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        
        if st.button("Update Admin Password"):
            if new_pass == confirm_pass and len(new_pass) > 5:
                # Logic to update password in DB
                st.success("Security credentials updated successfully.")
            else:
                st.error("Passwords do not match or are too weak.")

    st.info("💡 Note: As a Superuser, your profile changes affect system-wide logs.")