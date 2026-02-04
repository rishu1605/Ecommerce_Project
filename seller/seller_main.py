import streamlit as st
from seller.auth.auth_ui import render_seller_auth
import database as db

def run_seller_ui():
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "seller":
        render_seller_auth()
    else:
        # Check approval status
        seller_id = st.session_state.user_data['user_id']
        profile = db.fetch_query("SELECT status FROM seller_profiles WHERE seller_id=?", (seller_id,))
        status = profile['status'][0] if not profile.empty else "Unregistered"

        st.sidebar.title("🏪 Seller Studio")
        st.sidebar.info(f"Status: {status}")
        
        menu = st.sidebar.radio("Seller Menu", [
            "📊 Dashboard", "📦 Inventory", "📑 Shop Orders", "👤 Profile", "📞 Support"
        ])

        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()

        if status != "Approved" and menu == "📦 Inventory":
            st.warning("You must be approved by Admin to manage inventory.")
        else:
            # Routing to seller/inventory/inventory_ui.py etc.
            st.write(f"Opening {menu}...")