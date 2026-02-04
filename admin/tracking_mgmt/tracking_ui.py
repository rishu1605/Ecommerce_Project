import streamlit as st
import database as db

def render_order_tracking():
    st.title("📦 Global Order Tracking")
    
    # Master list of all transactions
    query = """
        SELECT o.order_id, b.name as buyer, s.name as seller, o.product_name, o.amount, o.status, o.date 
        FROM orders o
        JOIN users b ON o.buyer_id = b.user_id
        JOIN users s ON o.seller_id = s.user_id
        ORDER BY o.date DESC
    """
    all_orders = db.fetch_query(query)

    if all_orders.empty:
        st.write("No transactions recorded yet.")
    else:
        # Filters for Admin
        status_filter = st.multiselect("Filter by Status", ["Confirmed", "Shipped", "Delivered", "Cancelled"], default=["Confirmed"])
        filtered_df = all_orders[all_orders['status'].isin(status_filter)]
        
        st.dataframe(filtered_df, use_container_width=True)