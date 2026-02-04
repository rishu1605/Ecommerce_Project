import hashlib
import streamlit as st

def hash_password(password):
    """Securely hashes passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_session():
    """Checks if a user is logged in and returns their data."""
    if not st.session_state.get("logged_in"):
        return None
    return st.session_state.get("user_data")

def logout():
    """Clears the session and reloads the app."""
    st.session_state.clear()
    st.rerun()