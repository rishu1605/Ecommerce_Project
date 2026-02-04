import streamlit as st
from assets.theme import inject_global_css

# --- MODULE IMPORTS ---
# We import the entry point functions from each module's main file
from seller.seller_main import run_seller_ui
from buyer.buyer_main import run_buyer_ui
from admin.admin_main import run_admin_ui

def main():
    # 1. Page Configuration
    st.set_page_config(
        page_title="SIC Mart | Premium Marketplace",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Inject Aesthetic UI (Sapphire & Rose Gold)
    inject_global_css()

    # 3. Initialize Global Session States
    if "role" not in st.session_state:
        st.session_state.role = "Portal Home"
    
    # 4. Top Navigation / Persona Switcher
    # This remains visible until a user logs in to a specific high-security role
    with st.container():
        st.markdown("<div class='sic-mart-header'>SIC Mart</div>", unsafe_allow_html=True)
        
        # Simple persona selector for development/navigation
        cols = st.columns([1, 1, 1, 1, 1])
        with cols[1]:
            if st.button("🛍️ Shop Now", use_container_width=True):
                st.session_state.role = "Buyer"
        with cols[2]:
            if st.button("📦 Start Selling", use_container_width=True):
                st.session_state.role = "Seller"
        with cols[3]:
            if st.button("🛡️ Admin Panel", use_container_width=True):
                st.session_state.role = "Admin"
    
    st.markdown("---")

    # 5. Routing Logic (The Switchboard)
    if st.session_state.role == "Buyer":
        run_buyer_ui()
        
    elif st.session_state.role == "Seller":
        run_seller_ui()
        
    elif st.session_state.role == "Admin":
        run_admin_ui()
        
    else:
        # Default Welcome Landing Page
        render_welcome_screen()

def render_welcome_screen():
    st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h1 style='color: #ffd1da; font-family: Lora;'>Welcome to the Future of Commerce</h1>
            <p style='color: #cbd5e1; font-size: 18px;'>
                Experience a seamless marketplace designed with elegance and powered by automation.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Showcase a few features
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**Automated Payments**\n\nFunds held securely in Escrow until you're satisfied.")
    with c2:
        st.info("**Smart Tracking**\n\nReal-time logistics updates at every step of the journey.")
    with c3:
        st.info("**Premium Support**\n\nDirect dispute resolution and 24/7 moderation.")

if __name__ == "__main__":
    main()