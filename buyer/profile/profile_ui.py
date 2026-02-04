import streamlit as st
import database as db
from .profile_backend import get_full_buyer_profile, update_buyer_profile

def render_buyer_profile():
    st.markdown("<h2 style='color: #2E86C1;'>👤 My Account Profile</h2>", unsafe_allow_html=True)

    # 1. Session & Auth Check
    if "user_data" not in st.session_state:
        st.error("Please log in to view your profile.")
        return

    buyer_id = st.session_state.user_data.get('user_id')
    
    # 2. Fetch Fresh Data from Database
    # We fetch this every time the function runs to ensure we have the latest DB state
    profile_df = get_full_buyer_profile(buyer_id)
    
    if profile_df.empty:
        st.error("Profile data not found. Please try logging out and back in.")
        return

    # Convert to dictionary and clean None values
    raw_profile = profile_df.iloc[0].to_dict()
    profile = {k: (v if v is not None else "") for k, v in raw_profile.items()}
    
    # 3. Wallet Quick-View (Real-time)
    wallet_data = db.fetch_query("SELECT balance FROM wallets WHERE user_id = ?", (buyer_id,))
    balance = wallet_data['balance'][0] if not wallet_data.empty else 0.0
    
    col_metric, col_info = st.columns([1, 2])
    with col_metric:
        st.metric("Wallet Balance", f"₹{balance:,.2f}")
    with col_info:
        st.info("Your details are saved securely. Updates take effect immediately.")

    st.markdown("---")

    # 4. Profile Edit Form
    # clear_on_submit=False is important so data stays in fields if validation fails
    with st.form("buyer_profile_edit", clear_on_submit=False):
        st.markdown("#### 📍 Personal & Shipping Details")
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("Full Name", value=profile.get('name', ""))
            u_email = st.text_input("Email Address", value=profile.get('email', ""))
        with c2:
            # We use session_state for ID to ensure consistency
            st.text_input("Buyer ID (Fixed)", value=buyer_id, disabled=True)
            u_address = st.text_area("Shipping Address", value=profile.get('address', ""), height=68)

        st.markdown("---")

        st.markdown("#### 💳 Automated Refund Destinations")
        st.caption("Admin will use these details for any approved returns or wallet withdrawals.")
        
        u_upi = st.text_input("UPI ID (e.g., user@bank)", value=profile.get('upi_id', ""))
        
        st.markdown("**Bank Details (Optional)**")
        c3, c4 = st.columns(2)
        with c3:
            u_holder = st.text_input("Account Holder Name", value=profile.get('acc_holder', ""))
            u_acc = st.text_input("Account Number", value=profile.get('bank_acc', ""))
        with c4:
            u_ifsc = st.text_input("IFSC Code", value=profile.get('ifsc', ""))
            u_branch = st.text_input("Branch Name", value=profile.get('branch', ""))

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 5. Form Submission Button
        submit_btn = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)

    # 6. Logic handling
    if submit_btn:
        if not u_name or not u_email:
            st.error("Name and Email are mandatory.")
        else:
            formatted_ifsc = u_ifsc.upper().strip() if u_ifsc else ""
            
            # Update Database
            success, msg = update_buyer_profile(
                buyer_id, 
                u_name.strip(), 
                u_email.strip(), 
                u_address.strip(), 
                u_upi.strip(), 
                u_acc.strip(), 
                formatted_ifsc, 
                u_holder.strip(), 
                u_branch.strip()
            )
            
            if success:
                # IMPORTANT: Update st.session_state immediately
                # This ensures the Sidebar and other UI elements don't show old data
                st.session_state.user_data['name'] = u_name
                st.session_state.user_data['email'] = u_email
                
                st.success(f"✅ {msg}")
                # st.rerun() is critical here to refresh 'profile_df' in step 2
                st.rerun()
            else:
                st.error(f"❌ {msg}")