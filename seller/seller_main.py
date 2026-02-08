import streamlit as st
import database as db
from seller.auth.auth_ui import render_seller_auth

# Fixed Imports: Removed duplicates and consolidated
from seller.inventory.inventory_ui import show_inventory_listing, render_inventory_management
from seller.dashboard.dashboard_ui import render_seller_dashboard
from seller.profile.profile_ui import render_seller_profile # Matches the function in your profile_ui.py

def run_seller_ui():
    # 1. Authentication Check
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "seller":
        render_seller_auth()
    else:
        # 2. Extract and Normalize ID
        # Ensuring both 'user_id' and 'id' keys are available to prevent KeyError
        user_data = st.session_state.user_data
        seller_id = user_data.get('user_id') or user_data.get('id')
        
        # Inject 'id' into session_state because your render_seller_profile() requires it
        st.session_state.user_data['id'] = seller_id 

        # 3. Fetch Approval status from database
        profile = db.fetch_query("SELECT status FROM seller_profiles WHERE seller_id=?", (seller_id,))
        status = profile['status'][0] if not profile.empty else "Unregistered"

        # 4. Sidebar Navigation
        st.sidebar.title("🏪 Seller Studio")
        
        # Display Status with Color Coding
        if status == "Approved":
            st.sidebar.success(f"Status: {status}")
        else:
            st.sidebar.warning(f"Status: {status}")
        
        menu = st.sidebar.radio("Seller Menu", [
            "📊 Dashboard", "📦 Inventory", "📑 Shop Orders", "👤 Profile", "📞 Support"
        ])

        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        # 5. Content Routing Logic
        if menu == "📊 Dashboard":
            render_seller_dashboard()

        elif menu == "📦 Inventory":
            if status != "Approved":
                st.error("🚨 Access Denied: Your account must be 'Approved' by an Admin to list products.")
            else:
                tab1, tab2 = st.tabs(["➕ List New Item", "🛠️ Manage Existing Inventory"])
                with tab1:
                    show_inventory_listing()
                with tab2:
                    render_inventory_management()

        elif menu == "📑 Shop Orders":
            st.subheader("Order Management")
            # Integration point for order fulfillment

        elif menu == "👤 Profile":
            # Calling the specific function defined in your profile_ui.py
            render_seller_profile() 

        elif menu == "📞 Support":
            st.subheader("Seller Support Center")