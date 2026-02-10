import streamlit as st
from .profile_backend import get_full_seller_profile, update_seller_profile

def render_seller_profile():
    # 1. Pull ID from session state
    user_data = st.session_state.get('user_data', {})
    seller_id = user_data.get('id')
    
    profile_df = get_full_seller_profile(seller_id)
    
    if profile_df.empty:
        st.error("Profile not found.")
        return

    profile = profile_df.iloc[0]
    st.markdown("<div class='sic-mart-header' style='font-size: 30px !important;'>Business Profile</div>", unsafe_allow_html=True)

    # Use .get() or a simple if-else to handle None values from the database
    def safe_val(val):
        return str(val) if val is not None else ""

    with st.form("profile_edit_form"):
        # Section 1: Business Identity
        st.markdown("#### 🏢 Identity & Contact")
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("Owner Name", value=safe_val(profile['name']))
            u_store = st.text_input("Store Name", value=safe_val(profile['store_name']))
        with c2:
            u_email = st.text_input("Business Email", value=safe_val(profile['email']))
            # PAN is usually mandatory; kept as disabled per your original logic
            st.text_input("PAN (Permanent)", value=safe_val(profile['pan']), disabled=True)

        st.markdown("---")

        # Section 2: Banking
        st.markdown("#### 🏦 Payout Bank Details")
        c3, c4 = st.columns(2)
        with c3:
            u_holder = st.text_input("Account Holder Name", value=safe_val(profile['acc_holder']))
            u_acc = st.text_input("Account Number", value=safe_val(profile['bank_acc']))
        with c4:
            # FIX: Added safe_val and moved .upper() logic to handle None types
            raw_ifsc = st.text_input("IFSC Code", value=safe_val(profile['ifsc']))
            u_ifsc = raw_ifsc.upper()
            u_branch = st.text_input("Branch Name", value=safe_val(profile['branch']))

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Ensure the submit button is the LAST thing inside the 'with st.form' block
        submit_button = st.form_submit_button("Save Profile Changes", use_container_width=True)
        
        if submit_button:
            success, msg = update_seller_profile(
                seller_id, u_name, u_store, u_email, 
                u_acc, u_ifsc, u_branch, u_holder
            )
            
            if success:
                st.success(msg)
                st.session_state.user_data['name'] = u_name
                st.rerun()
            else:
                st.error(msg)