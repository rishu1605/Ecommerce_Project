import streamlit as st
import database as db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def handle_seller_login(email, password):
    hp = hash_password(password)
    query = "SELECT * FROM users WHERE email=? AND password=? AND role='seller'"
    user = db.fetch_query(query, (email, hp))
    
    if not user.empty:
        st.session_state.user_data = user.iloc[0].to_dict()
        st.session_state.role = 'seller'
        st.session_state.logged_in = True
        st.success("Welcome to your Storefront!")
        st.rerun()
    else:
        st.error("Invalid credentials or account does not exist.")

def handle_seller_registration(name, email, store, gst, pan, password):
    hp = hash_password(password)
    try:
        # 1. Create User Entry
        db.execute_query(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'seller')",
            (name, email, hp)
        )
        
        # 2. Get the new ID to link profile
        new_user = db.fetch_query("SELECT user_id FROM users WHERE email=?", (email,))
        s_id = int(new_user['user_id'][0])
        
        # 3. Create Seller Profile (Pending status)
        db.execute_query(
            "INSERT INTO seller_profiles (seller_id, store_name, gst_number, pan_number, status) VALUES (?, ?, ?, ?, 'Pending')",
            (s_id, store, gst, pan)
        )
        
        # 4. Create Seller Wallet
        db.execute_query("INSERT INTO wallets (user_id, balance) VALUES (?, 0.0)", (s_id,))
        
        st.success("Registration Successful! Admin will verify your GST/PAN details shortly.")
    except Exception as e:
        st.error(f"Registration Error: {e}")