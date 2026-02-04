import streamlit as st
import database as db

def render_order_history():
    """
    Displays order history and restores the data view.
    """
    st.markdown("<h3 style='color: #2E86C1;'>📜 My Order History</h3>", unsafe_allow_html=True)
    
    # Using 'user_id' which we synced in database.py
    buyer_id = st.session_state.user_data['user_id']
    
    try:
        # We try to fetch orders. If the table is empty, we show a clean message.
        query = "SELECT order_id, product_name, amount, status, date FROM orders WHERE buyer_id = ?"
        orders = db.fetch_query(query, (buyer_id,))
        
        if orders.empty:
            st.info("You haven't placed any orders yet. Once you buy something, it will appear here!")
        else:
            st.dataframe(orders, use_container_width=True, hide_index=True)
            
    except Exception:
        # Fallback if the 'orders' table hasn't been created yet in your DB
        st.warning("Order tracking system is initializing. Please check back after your first purchase.")