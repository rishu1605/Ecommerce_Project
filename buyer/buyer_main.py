import streamlit as st
# Absolute imports are safer in Streamlit multi-folder projects
from buyer.auth.auth_ui import render_buyer_auth
from buyer.orders.orders_ui import render_order_history
from buyer.wallet.wallet_ui import render_wallet_ui
from buyer.profile.profile_ui import render_buyer_profile
from buyer.home.home_ui import render_marketplace 
from buyer.cart.cart_ui import render_cart_ui, render_buy_now_payment

def run_buyer_ui():
    # 1. AUTH CHECK
    # Match the key 'role' used in your login logic
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "buyer":
        render_buyer_auth()
        return

    # 2. SIDEBAR NAVIGATION
    # Applied a bit of styling to the sidebar title to match your aesthetic
    st.sidebar.markdown("<h2 style='color: #f1f5f9;'>🛍️ Buyer Panel</h2>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio(
        "Navigation", 
        ["🏠 Home", "📦 My Orders", "🛒 Cart", "👛 Wallet", "👤 My Profile", "📞 Support"]
    )

    # 3. STATE MANAGEMENT
    # Reset Buy Now if the user navigates away from Home
    if menu != "🏠 Home":
        st.session_state.buy_now_active = False

    # 4. ROUTING LOGIC
    if st.session_state.get("buy_now_active") and menu == "🏠 Home":
        render_buy_now_payment()
    elif menu == "🏠 Home":
        render_marketplace() 
    elif menu == "📦 My Orders":
        render_order_history()
    elif menu == "🛒 Cart":
        render_cart_ui() 
    elif menu == "👛 Wallet":
        render_wallet_ui()
    elif menu == "👤 My Profile":
        render_buyer_profile()
    elif menu == "📞 Support":
        render_support_page() # Moved to a local style call

    # 5. LOGOUT
    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

def render_support_page():
    st.title("📞 Support")
    with st.container(border=True):
        st.write("### How can we help?")
        st.write("📧 **Email:** support@sicmart.com")
        st.write("💬 **Live Chat:** Available 10 AM - 6 PM")
        st.info("Please include your Order ID for faster resolution.")