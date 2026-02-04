import streamlit as st

# Import the UI components
from buyer.auth.auth_ui import render_buyer_auth
from buyer.orders.orders_ui import render_order_history
from buyer.wallet.wallet_ui import render_wallet_ui
from buyer.profile.profile_ui import render_buyer_profile
# from buyer.home.home_ui import render_marketplace  # Uncomment when home_ui is ready
# from buyer.cart.cart_ui import render_cart_ui      # Uncomment when cart_ui is ready

def run_buyer_ui():
    # 1. Authentication Check
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "buyer":
        render_buyer_auth()
    else:
        # 2. Sidebar Navigation
        st.sidebar.title("🛍️ Buyer Panel")
        
        # Display User Name and Balance in Sidebar for convenience
        user_name = st.session_state.user_data.get('name', 'User')
        st.sidebar.write(f"Welcome, **{user_name}**")
        
        st.sidebar.markdown("---")
        
        menu = st.sidebar.radio("Navigation", [
            "🏠 Home", 
            "📦 My Orders", 
            "🛒 Cart", 
            "👛 Wallet", 
            "👤 My Profile", 
            "📞 Support"
        ])
        
        st.sidebar.markdown("---")
        if st.sidebar.button("🔓 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        # 3. Routing Logic (The Handshake)
        if menu == "🏠 Home":
            st.title("🏙️ Marketplace")
            st.info("Browsing all available products...")
            # render_marketplace() 

        elif menu == "📦 My Orders":
            render_order_history()

        elif menu == "🛒 Cart":
            st.title("🛒 Your Shopping Cart")
            # render_cart_ui()

        elif menu == "👛 Wallet":
            render_wallet_ui()

        elif menu == "👤 My Profile":
            # This was the missing part! Calling the actual function.
            render_buyer_profile()

        elif menu == "📞 Support":
            st.title("📞 Contact Support")
            with st.container(border=True):
                st.write("Need help with an order or your wallet?")
                st.write("📧 Email: support@sicmart.com")
                st.write("📱 Toll-Free: 1800-SIC-MART")
                st.text_area("Drop us a message")
                if st.button("Send Message"):
                    st.success("Ticket raised! We will contact you shortly.")