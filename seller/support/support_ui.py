import streamlit as st
from .support_backend import get_forwarded_complaints, resolve_complaint

def render_support_hub():
    seller_id = st.session_state.user_data['id']
    st.markdown("<div class='sic-mart-header' style='font-size: 30px !important;'>Support Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='dynamic-subheader'>Buyer Issues Forwarded by Admin</div>", unsafe_allow_html=True)

    complaints = get_forwarded_complaints(seller_id)

    if complaints.empty:
        st.success("✨ No active complaints. Your customers are happy!")
    else:
        for _, row in complaints.iterrows():
            with st.container(): # Glassmorphic Card
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Ticket ID:** `#{row['id']}` | **Order:** `{row['order_id']}`")
                    st.markdown(f"**Buyer:** {row['buyer_name']}")
                    st.error(f"**Subject:** {row['subject']}")
                    st.info(f"**Message:** {row['message']}")
                
                with col2:
                    st.caption(f"Received: {row['created_at']}")
                    # Action Modal / Expander
                    with st.expander("Respond"):
                        res_text = st.text_area("Resolution Details", key=f"res_{row['id']}")
                        if st.button("Submit Resolution", key=f"btn_{row['id']}", use_container_width=True):
                            if res_text:
                                resolve_complaint(row['id'], res_text)
                                st.success("Resolution sent to Admin for final closing.")
                                st.rerun()
                            else:
                                st.warning("Please enter details.")
                
                st.markdown("<hr style='opacity: 0.1;'>", unsafe_allow_html=True)