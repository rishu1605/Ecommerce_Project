import streamlit as st
import database as db
from .profile_backend import get_full_buyer_profile, update_buyer_profile

def render_buyer_profile():
    # --- 1. AESTHETIC CSS INJECTION ---
    st.markdown("""
        <style>
        /* Global Background: Professional Slate */
        .stApp {
            background-color: #0f172a; /* Deep Slate/Navy */
        }

        /* Wallet Card: Warm Aesthetic Gradient */
        .wallet-card {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            padding: 24px;
            border-radius: 16px;
            color: white !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .wallet-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 600;
            opacity: 0.9;
        }
        .wallet-balance {
            font-size: 2.2rem;
            font-weight: 800;
            font-family: 'Inter', sans-serif;
            margin-top: 4px;
        }

        /* Info Box Styling */
        .info-container {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #3b82f6;
            color: #cbd5e1;
            font-size: 0.95rem;
        }

        /* Input Field Styling for Slate Theme */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #334155 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 2. SESSION & AUTH CHECK ---
    if "user_data" not in st.session_state:
        st.error("Please log in to view your profile.")
        return

    buyer_id = st.session_state.user_data.get('user_id')
    
    # 3. Fetch Fresh Data
    profile_df = get_full_buyer_profile(buyer_id)
    if profile_df.empty:
        st.error("Profile data not found.")
        return

    raw_profile = profile_df.iloc[0].to_dict()
    profile = {k: (v if v is not None else "") for k, v in raw_profile.items()}
    
    # Fetch Balance
    wallet_data = db.fetch_query("SELECT balance FROM wallets WHERE user_id = ?", (buyer_id,))
    balance = wallet_data['balance'][0] if not wallet_data.empty else 0.0

    # --- 4. HEADER & WALLET QUICK-VIEW ---
    st.markdown("<h1 style='color: #f8fafc; margin-bottom: 20px;'>👤 My Account Profile</h1>", unsafe_allow_html=True)
    
    col_wallet, col_note = st.columns([1, 1.5])
    
    with col_wallet:
        # Fixed: The Warm Gradient Wallet Card
        st.markdown(f"""
            <div class="wallet-card">
                <div class="wallet-label">Total Balance</div>
                <div class="wallet-balance">₹{balance:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_note:
        st.markdown(f"""
            <div class="info-container">
                <b>Secure Account</b><br>
                Your details are encrypted and saved securely. 
                Changes to your shipping address take effect immediately on new orders.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 0.5px solid #334155;'>", unsafe_allow_html=True)

    # --- 5. PROFILE EDIT FORM ---
    with st.form("buyer_profile_edit", clear_on_submit=False):
        st.markdown("<h4 style='color: #94a3b8;'>📍 Personal & Shipping Details</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("Full Name", value=profile.get('name', ""))
            u_email = st.text_input("Email Address", value=profile.get('email', ""))
        with c2:
            st.text_input("Buyer ID (Fixed Account)", value=f"USER-{buyer_id}", disabled=True)
            u_address = st.text_area("Shipping Address", value=profile.get('address', ""), height=68)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #94a3b8;'>💳 Automated Refund Destinations</h4>", unsafe_allow_html=True)
        st.caption("Used for approved returns or wallet withdrawals.")
        
        u_upi = st.text_input("UPI ID (e.g., username@okaxis)", value=profile.get('upi_id', ""))
        
        st.markdown("<p style='font-weight: bold; color: #cbd5e1; margin-top: 10px;'>Bank Details (Optional)</p>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            u_holder = st.text_input("Account Holder Name", value=profile.get('acc_holder', ""))
            u_acc = st.text_input("Account Number", value=profile.get('bank_acc', ""))
        with c4:
            u_ifsc = st.text_input("IFSC Code", value=profile.get('ifsc', ""))
            u_branch = st.text_input("Branch Name", value=profile.get('branch', ""))

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)

    # --- 6. LOGIC HANDLING ---
    if submit_btn:
        if not u_name or not u_email:
            st.error("Name and Email are mandatory.")
        else:
            formatted_ifsc = u_ifsc.upper().strip() if u_ifsc else ""
            
            success, msg = update_buyer_profile(
                buyer_id, u_name.strip(), u_email.strip(), u_address.strip(), 
                u_upi.strip(), u_acc.strip(), formatted_ifsc, 
                u_holder.strip(), u_branch.strip()
            )
            
            if success:
                st.session_state.user_data['name'] = u_name
                st.session_state.user_data['email'] = u_email
                st.success(f"✅ {msg}")
                st.rerun()
            else:
                st.error(f"❌ {msg}")