import streamlit as st
import database as db

def render_seller_dashboard():
    seller_id = st.session_state.user_data['user_id']
    
    st.markdown(f"<h2>Welcome back, {st.session_state.user_data['name']}!</h2>", unsafe_allow_html=True)
    
    # Fetch Data for Metrics
    wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id = ?", (seller_id,))
    orders = db.fetch_query("SELECT COUNT(*) as count, SUM(amount) as revenue FROM orders WHERE seller_id = ?", (seller_id,))
    
    bal = wallet['balance'][0] if not wallet.empty else 0.0
    total_orders = orders['count'][0] if not orders.empty else 0
    total_rev = orders['revenue'][0] if orders['revenue'][0] is not None else 0.0

    # Display Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Wallet Balance", f"₹{bal:,.2f}")
    m2.metric("Total Orders", total_orders)
    m3.metric("Total Revenue", f"₹{total_rev:,.2f}")

    st.markdown("---")
    
    # Quick View of Recent Sales
    st.subheader("Recent Sales activity")
    recent = db.fetch_query(
        "SELECT product_name, amount, status, date FROM orders WHERE seller_id = ? ORDER BY date DESC LIMIT 5", 
        (seller_id,)
    )
    
    if recent.empty:
        st.write("No sales yet. Once customers buy your products, they'll show up here!")
    else:
        st.table(recent)