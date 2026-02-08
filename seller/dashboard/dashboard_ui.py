import streamlit as st
import database as db

def render_seller_dashboard():
    # 1. Custom CSS for Light-Themed Metric Tiles
    st.markdown("""
        <style>
            /* Main Dashboard Heading */
            .dashboard-title {
                color: #1E1E1E;
                font-weight: 700;
                margin-bottom: 20px;
            }

            /* Target the Metric Labels (e.g., 'Wallet Balance') */
            [data-testid="stMetricLabel"] {
                color: #555555 !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
            }

            /* Target the Metric Values (e.g., '₹0.00') */
            [data-testid="stMetricValue"] {
                color: #000000 !important;
                font-size: 1.8rem !important;
                font-weight: 800 !important;
            }

            /* Style the columns to look like elevated white cards */
            div[data-testid="stHorizontalBlock"] > div {
                background-color: #ffffff;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                border: 1px solid #f0f2f6;
            }
        </style>
    """, unsafe_allow_html=True)

    # Use the normalized ID from previous steps
    seller_id = st.session_state.user_data.get('id') or st.session_state.user_data.get('user_id')
    
    st.markdown(f"<h2 class='dashboard-title'>Welcome back, {st.session_state.user_data['name']}!</h2>", unsafe_allow_html=True)
    
    # Fetch Data
    wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id = ?", (seller_id,))
    orders = db.fetch_query("SELECT COUNT(*) as count, SUM(amount) as revenue FROM orders WHERE seller_id = ?", (seller_id,))
    
    bal = wallet['balance'][0] if not wallet.empty else 0.0
    total_orders = orders['count'][0] if not orders.empty else 0
    total_rev = orders['revenue'][0] if orders['revenue'][0] is not None else 0.0

    # Display Metrics in Styled Tiles
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Wallet Balance", f"₹{bal:,.2f}")
    with m2:
        st.metric("Total Orders", total_orders)
    with m3:
        st.metric("Total Revenue", f"₹{total_rev:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Recent Activity Section
    st.subheader("Recent Sales Activity")
    recent = db.fetch_query(
        "SELECT product_name as 'Product', amount as 'Amount (₹)', status as 'Status', date as 'Date' "
        "FROM orders WHERE seller_id = ? ORDER BY date DESC LIMIT 5", 
        (seller_id,)
    )
    
    if recent.empty:
        st.info("No sales yet. Once customers buy your products, they'll show up here!")
    else:
        # Using dataframe instead of table for better styling
        st.dataframe(recent, use_container_width=True, hide_index=True)