import streamlit as st
import database as db

# Import specific UI modules from your admin subfolders
from admin.dashboard.dashboard_ui import render_admin_dashboard
from admin.user.user_ui import render_user_mgmt
from admin.catalog.catalog_ui import render_admin_catalog
from admin.finance.finance_ui import render_finance_mgmt

def run_admin_ui():
    st.sidebar.title("🛡️ Admin Panel")
    choice = st.sidebar.radio("Navigation", [
        "Dashboard", 
        "Approve Sellers", 
        "Catalog Management", 
        "Platform Finance"
    ])

    if choice == "Dashboard":
        render_admin_dashboard()
    
    elif choice == "Approve Sellers":
        render_seller_approvals()
    
    elif choice == "Catalog Management":
        render_admin_catalog()
    
    elif choice == "Platform Finance":
        render_finance_mgmt()

def render_seller_approvals():
    st.header("📝 Pending Seller Approvals")
    
    # Fetch sellers who are still 'Pending'
    query = "SELECT * FROM seller_profiles WHERE status = 'Pending'"
    pending_sellers = db.fetch_query(query)

    if pending_sellers.empty:
        st.success("No pending approvals!")
    else:
        for index, row in pending_sellers.iterrows():
            with st.expander(f"Store: {row['store_name']} (Seller ID: {row['seller_id']})"):
                st.write(f"**GST:** {row['gst_number']}")
                st.write(f"**PAN:** {row['pan_number']}")
                
                col1, col2 = st.columns(2)
                if col1.button("Approve", key=f"app_{row['seller_id']}"):
                    db.execute_query(
                        "UPDATE seller_profiles SET status = 'Approved' WHERE seller_id = ?", 
                        (row['seller_id'],)
                    )
                    st.success(f"Approved {row['store_name']}")
                    st.rerun()
                
                if col2.button("Reject", key=f"rej_{row['seller_id']}", type="primary"):
                    db.execute_query(
                        "UPDATE seller_profiles SET status = 'Rejected' WHERE seller_id = ?", 
                        (row['seller_id'],)
                    )
                    st.error(f"Rejected {row['store_name']}")
                    st.rerun()