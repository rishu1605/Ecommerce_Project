import streamlit as st
import database as db
import hashlib

def hash_password(password):
    """Encodes the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def handle_buyer_login(email, password):
    """
    Authenticates the buyer and stores data in session_state.
    Matches the schema: user_id, name, email, password, role.
    """
    hashed_pw = hash_password(password)
    query = "SELECT * FROM users WHERE email = ? AND password = ? AND role = 'buyer'"
    
    try:
        user_df = db.fetch_query(query, (email, hashed_pw))
        if not user_df.empty:
            # Converts the SQL row into a dictionary (includes 'user_id')
            st.session_state.user_data = user_df.iloc[0].to_dict()
            st.session_state.role = 'buyer'
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid email or password. Please try again.")
    except Exception as e:
        st.error(f"Authentication Error: {e}")

def handle_buyer_registration(name, email, password):
    """
    Registers a new buyer account into the database.
    """
    hashed_pw = hash_password(password)
    
    try:
        # Check if email is already taken
        existing = db.fetch_query("SELECT email FROM users WHERE email = ?", (email,))
        if not existing.empty:
            st.warning("This email is already registered. Please login.")
            return

        # Insert record
        db.execute_query(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'buyer')",
            (name, email, hashed_pw)
        )
        st.success("Registration Successful! Switch to the Login tab to continue.")
    except Exception as e:
        st.error(f"Registration Failed: {e}")