import streamlit as st
import database as db
from seller.auth.auth_ui import render_seller_auth
# Import your UI modules here
from seller.inventory.inventory_ui import show_inventory_listing

def run_seller_ui():
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "seller":
        render_seller_auth()
    else:
        # Check approval status from database
        seller_id = st.session_state.user_data['user_id']
        profile = db.fetch_query("SELECT status FROM seller_profiles WHERE seller_id=?", (seller_id,))
        status = profile['status'][0] if not profile.empty else "Unregistered"

        # Sidebar Navigation
        st.sidebar.title("🏪 Seller Studio")
        
        # Display Status with Color Coding
        if status == "Approved":
            st.sidebar.success(f"Status: {status}")
        else:
            st.sidebar.warning(f"Status: {status}")
        
        menu = st.sidebar.radio("Seller Menu", [
            "📊 Dashboard", "📦 Inventory", "📑 Shop Orders", "👤 Profile", "📞 Support"
        ])

        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()

        # Content Routing Logic
        if menu == "📊 Dashboard":
            st.subheader("Seller Performance Overview")
            # Call your dashboard function here

        elif menu == "📦 Inventory":
            if status != "Approved":
                st.error("🚨 Access Denied: Your account must be 'Approved' by an Admin to list products.")
            else:
                # This calls the listing form we built
                show_inventory_listing()

        elif menu == "📑 Shop Orders":
            st.subheader("Order Management")
            # from seller.sales.sales_ui import show_orders
            # show_orders()

        elif menu == "👤 Profile":
            st.subheader("Business Profile")
            # from seller.profile.profile_ui import show_seller_profile
            # show_seller_profile()

        elif menu == "📞 Support":
            st.subheader("Seller Support Center")
            # from seller.support.support_ui import show_seller_support
            # show_seller_support()