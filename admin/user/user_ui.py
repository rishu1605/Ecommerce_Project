import streamlit as st
import database as db

def render_user_mgmt():
    st.markdown("<h2 style='color: #0F52BA;'>👥 User & Seller Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✅ Seller Verification", "📋 All Users"])

    with tab1:
        st.subheader("Pending Verifications")
        # Fetch only pending sellers using the JOIN logic you provided
        query = '''
            SELECT u.user_id, u.name, s.store_name, s.gst_number, s.pan_number, s.status 
            FROM users u 
            JOIN seller_profiles s ON u.user_id = s.seller_id 
            WHERE s.status = 'Pending'
        '''
        pending = db.fetch_query(query)
        
        if pending.empty:
            st.success("All caught up! No pending verifications.")
        else:
            for index, row in pending.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['store_name']}")
                        st.write(f"**Owner:** {row['name']} | **ID:** `{row['user_id']}`")
                        st.code(f"GST: {row['gst_number']} | PAN: {row['pan_number']}")
                    with col2:
                        st.write("") # Padding
                        if st.button("✅ Approve", key=f"app_{row['user_id']}", use_container_width=True):
                            db.execute_query("UPDATE seller_profiles SET status='Approved' WHERE seller_id=?", (row['user_id'],))
                            st.toast(f"Approved {row['store_name']}!")
                            st.rerun()
                        if st.button("❌ Reject", key=f"rej_{row['user_id']}", use_container_width=True, type="secondary"):
                            db.execute_query("UPDATE seller_profiles SET status='Rejected' WHERE seller_id=?", (row['user_id'],))
                            st.error(f"Rejected {row['store_name']}")
                            st.rerun()

    with tab2:
        st.subheader("System User Directory")
        all_users = db.fetch_query("SELECT user_id, name, email, role FROM users")
        st.dataframe(all_users, use_container_width=True, hide_index=True)
        
        if not all_users.empty:
            with st.expander("🛠️ Dangerous Actions"):
                user_to_del = st.selectbox("Select User ID to Wipe", all_users['user_id'].tolist())
                if st.button("Permanent Delete User", type="primary"):
                    db.execute_query("DELETE FROM users WHERE user_id=?", (user_to_del,))
                    st.success("User removed from system.")
                    st.rerun()