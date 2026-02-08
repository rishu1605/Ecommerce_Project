import streamlit as st
import database as db
from .profile_backend import get_full_buyer_profile, update_buyer_profile

def render_buyer_profile():
    # --- 1. PREMIUM AESTHETIC CSS ---
    st.markdown("""
        <style>
        /* Global Background and Typography */
        .stApp { background-color: #0f172a; }
        
        /* Glassmorphism Profile Header */
        .profile-hero {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            padding: 30px;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 25px;
        }
        
        .profile-avatar {
            width: 80px; height: 80px;
            background: linear-gradient(45deg, #6366F1, #A855F7);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 40px; color: white;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
        }

        /* Wallet Card: Vibrant Gold Gradient */
        .wallet-card {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            padding: 24px;
            border-radius: 20px;
            color: white !important;
            box-shadow: 0 10px 25px -5px rgba(217, 119, 6, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .section-header {
            color: #6366F1;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-size: 0.85rem;
            margin-bottom: 15px;
        }

        /* Modern Input Container */
        div[data-testid="stForm"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. SESSION & AUTH CHECK
    if "user_data" not in st.session_state:
        st.error("Please log in to view your profile.")
        return

    buyer_id = st.session_state.user_data.get('user_id')
    
    # 3. DATA FETCHING
    profile_df = get_full_buyer_profile(buyer_id)
    if profile_df.empty:
        st.error("Profile data not found.")
        return

    raw_profile = profile_df.iloc[0].to_dict()
    profile = {k: (v if v is not None else "") for k, v in raw_profile.items()}
    
    wallet_data = db.fetch_query("SELECT balance FROM wallets WHERE user_id = ?", (buyer_id,))
    balance = wallet_data['balance'][0] if not wallet_data.empty else 0.0

    # --- 4. VISUAL HERO SECTION ---
    st.markdown(f"""
        <div class="profile-hero">
            <div class="profile-avatar">👤</div>
            <div>
                <h1 style='color: white; margin: 0; font-size: 1.8rem;'>{profile.get('name', 'User')}</h1>
                <p style='color: #94a3b8; margin: 0;'>Member ID: USER-{buyer_id} | Verified Account</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 5. WALLET & STATUS ROW ---
    col_w, col_s = st.columns([1, 1.5], gap="large")
    
    with col_w:
        st.markdown(f"""
            <div class="wallet-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.8; font-weight: 600;">Wallet Balance</div>
                <div style="font-size: 2.4rem; font-weight: 800; margin-top: 5px;">₹{balance:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_s:
        with st.container(border=True):
            st.markdown("**🛡️ Account Security**")
            st.caption("Your details are encrypted. Changes to your shipping address will update instantly.")
            st.info("💡 Tip: Add your UPI ID for faster automated refunds.")

    st.write("---")

    # --- 6. PROFILE EDIT FORM ---
    with st.form("buyer_profile_edit"):
        # Section 1: Identity
        st.markdown('<div class="section-header">📍 Personal & Shipping</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("Full Name", value=profile.get('name', ""), help="Your display name on invoices.")
            u_email = st.text_input("Email Address", value=profile.get('email', ""))
        with c2:
            u_address = st.text_area("Default Shipping Address", value=profile.get('address', ""), height=100)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Section 2: Financials
        st.markdown('<div class="section-header">💳 Refund & Bank Details</div>', unsafe_allow_html=True)
        u_upi = st.text_input("UPI ID", value=profile.get('upi_id', ""), placeholder="username@upi")
        
        with st.expander("🏦 Configure Bank Account (Optional)"):
            c3, c4 = st.columns(2)
            with c3:
                u_holder = st.text_input("Account Holder Name", value=profile.get('acc_holder', ""))
                u_acc = st.text_input("Account Number", value=profile.get('bank_acc', ""))
            with c4:
                u_ifsc = st.text_input("IFSC Code", value=profile.get('ifsc', ""))
                u_branch = st.text_input("Branch Name", value=profile.get('branch', ""))

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action Button
        submit_btn = st.form_submit_button("💾 Update My Account Profile", use_container_width=True, type="primary")

    # --- 7. LOGIC HANDLING ---
    if submit_btn:
        if not u_name or not u_email:
            st.error("Mandatory fields (Name & Email) cannot be empty.")
        else:
            success, msg = update_buyer_profile(
                buyer_id, u_name.strip(), u_email.strip(), u_address.strip(), 
                u_upi.strip(), u_acc.strip(), u_ifsc.upper().strip(), 
                u_holder.strip(), u_branch.strip()
            )
            
            if success:
                st.session_state.user_data['name'] = u_name
                st.session_state.user_data['email'] = u_email
                st.toast("Profile Updated Successfully!")
                st.success(f"✅ {msg}")
                st.rerun()
            else:
                st.error(f"❌ {msg}")