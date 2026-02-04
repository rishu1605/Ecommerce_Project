import streamlit as st
from .profile_backend import get_full_seller_profile, update_seller_profile

def render_seller_profile():
    seller_id = st.session_state.user_data['id']
    profile_df = get_full_seller_profile(seller_id)
    
    if profile_df.empty:
        st.error("Profile not found.")
        return

    profile = profile_df.iloc[0]
    st.markdown("<div class='sic-mart-header' style='font-size: 30px !important;'>Business Profile</div>", unsafe_allow_html=True)

    with st.form("profile_edit_form"):
        # Section 1: Business Identity
        st.markdown("#### 🏢 Identity & Contact")
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("Owner Name", value=profile['name'])
            u_store = st.text_input("Store Name", value=profile['store_name'])
        with c2:
            u_email = st.text_input("Business Email", value=profile['email'])
            st.text_input("PAN (Permanent)", value=profile['pan'], disabled=True, help="Contact Admin to change PAN")

        st.markdown("---")

        # Section 2: Banking (The Payout Destination)
        st.markdown("#### 🏦 Payout Bank Details")
        c3, c4 = st.columns(2)
        with c3:
            u_holder = st.text_input("Account Holder Name", value=profile['acc_holder'])
            u_acc = st.text_input("Account Number", value=profile['bank_acc'])
        with c4:
            u_ifsc = st.text_input("IFSC Code", value=profile['ifsc']).upper()
            u_branch = st.text_input("Branch Name", value=profile['branch'])

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit Button with Rose Gold Styling
        if st.form_submit_button("Save Profile Changes", use_container_width=True):
            success, msg = update_seller_profile(
                seller_id, u_name, u_store, u_email, 
                u_acc, u_ifsc, u_branch, u_holder
            )
            if success:
                st.success(msg)
                # Update the local session name in case it changed
                st.session_state.user_data['name'] = u_name
                st.rerun()
            else:
                st.error(msg)