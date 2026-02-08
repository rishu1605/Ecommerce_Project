import streamlit as st
# Absolute imports for the Buyer module components
from buyer.auth.auth_ui import render_buyer_auth
from buyer.orders.orders_ui import render_order_history
from buyer.wallet.wallet_ui import render_wallet_ui
from buyer.profile.profile_ui import render_buyer_profile
from buyer.home.home_ui import render_marketplace 
from buyer.cart.cart_ui import render_cart_ui, render_buy_now_payment

def render_support_page():
    """Fallback Support UI if the external module is missing"""
    st.title("📞 Support")
    with st.container(border=True):
        st.write("### How can we help?")
        st.write("📧 **Email:** support@sicmart.com")
        st.write("💬 **Live Chat:** Available 10 AM - 6 PM")
        st.info("Please include your Order ID for faster resolution.")

def run_buyer_ui():
    # 1. AUTHENTICATION CHECK
    # Match both 'logged_in' and 'role' session keys
    if not st.session_state.get("logged_in") or st.session_state.get("role") != "buyer":
        render_buyer_auth()
        return

    # 2. SIDEBAR STYLING (High Contrast for SIC Mart)
    st.sidebar.markdown("""
        <style>
        /* Force Sidebar Radio labels to Dark Black for high visibility */
        div[data-testid="stSidebar"] .stRadio label p {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        /* Sidebar Title Branding */
        .sb-title { 
            color: #000000; 
            font-size: 1.6rem; 
            font-weight: 900; 
            text-align: center; 
            margin-bottom: 0px;
        }
        </style>
        <div class="sb-title">🛍️ SIC Mart</div>
        <div style="text-align:center; font-weight:700; color:#444; margin-bottom:10px;">BUYER PANEL</div>
        <hr style="border-top: 2px solid #000; margin-top:0px;">
    """, unsafe_allow_html=True)
    
    # 3. NAVIGATION MENU
    menu = st.sidebar.radio(
        "Navigation", 
        ["🏠 Home", "📦 My Orders", "🛒 Cart", "👛 Wallet", "👤 My Profile", "📞 Support"],
        label_visibility="collapsed"
    )

    # 4. STATE MANAGEMENT
    # Reset Buy Now if the user navigates away from Home
    if menu != "🏠 Home":
        st.session_state.buy_now_active = False

    # 5. ROUTING LOGIC (All features preserved)
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
        # Attempt to load the external support UI, fallback to local if it fails
        try:
            from buyer.support.support_ui import render_support_ui
            render_support_ui()
        except (ImportError, ModuleNotFoundError):
            render_support_page()

    # 6. LOGOUT
    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()