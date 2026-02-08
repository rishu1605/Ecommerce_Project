import streamlit as st
from .orders_backend import get_seller_orders, update_order_status

def render_orders_management():
    st.title("📦 Order Management")
    
    # Resolve the seller_id from session state
    user_data = st.session_state.get('user_data', {})
    seller_id = user_data.get('user_id') or user_data.get('id')
    
    if not seller_id:
        st.error("User session lost. Please log in again.")
        return

    orders_df = get_seller_orders(seller_id)

    if orders_df is None or orders_df.empty:
        st.info(f"No orders found for Seller ID: {seller_id}")
        # Add a diagnostic button
        if st.checkbox("Show Debug Info"):
            st.write("Current Session Data:", user_data)
        return

    # Render the orders
    for _, row in orders_df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"{row['product_name']}")
                st.write(f"**Order ID:** {row['order_id']} | **Customer:** {row['customer_name']}")
                st.write(f"**Address:** {row['shipping_address']}")
                st.caption(f"Date: {row['date']}")
            with col2:
                st.metric("Total", f"₹{row['amount']}")
                
                # Status Update Dropdown
                current_status = row['status']
                options = ["Confirmed", "Shipped", "Delivered", "Cancelled"]
                if current_status not in options: options.append(current_status)
                
                new_status = st.selectbox("Update", options, index=options.index(current_status), key=f"s_{row['order_id']}")
                
                if st.button("Apply", key=f"b_{row['order_id']}"):
                    update_order_status(row['order_id'], new_status)
                    st.success("Updated!")
                    st.rerun()