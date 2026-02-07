import streamlit as st
from buyer.auth.auth_ui import render_buyer_auth
from buyer.orders.orders_ui import render_order_history
from buyer.wallet.wallet_ui import render_wallet_ui
from buyer.profile.profile_ui import render_buyer_profile
from buyer.home.home_ui import render_marketplace 
from buyer.cart.cart_ui import render_cart_ui, render_buy_now_payment

def run_buyer_ui():
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "buyer":
        render_buyer_auth()
        return

    st.sidebar.title("🛍️ Buyer Panel")
    menu = st.sidebar.radio("Navigation", ["🏠 Home", "📦 My Orders", "🛒 Cart", "👛 Wallet", "👤 My Profile", "📞 Support"])

    # Safety: Reset Buy Now if switching pages
    if menu != "🏠 Home":
        st.session_state.buy_now_active = False

    # Route to Buy Now if active
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
        st.title("📞 Support")
        st.write("📧 support@sicmart.com")

    if st.sidebar.button("🔓 Logout"):
        st.session_state.clear()
        st.rerun()