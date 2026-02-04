import streamlit as st
import database as db

def render_finance_mgmt():
    st.title("💰 Platform Finance Manager")
    
    # 1. Total Platform Liquidity
    total_liquidity = db.fetch_query("SELECT SUM(balance) as total FROM wallets")
    
    # 2. Total Sales Volume
    total_sales = db.fetch_query("SELECT SUM(amount) as total FROM orders")
    
    # 3. Platform Revenue (Assuming a 10% commission model)
    platform_revenue = (total_sales['total'][0] or 0) * 0.10

    col1, col2, col3 = st.columns(3)
    col1.metric("Total User Funds", f"₹{total_liquidity['total'][0]:,.2f}")
    col2.metric("Gross Merchandise Value", f"₹{total_sales['total'][0]:,.2f}")
    col3.metric("Platform Earnings (10%)", f"₹{platform_revenue:,.2f}")

    st.markdown("---")
    st.subheader("Global Wallet Audit")
    wallets = db.fetch_query('''
        SELECT u.user_id, u.name, u.role, w.balance 
        FROM users u 
        JOIN wallets w ON u.user_id = w.user_id
    ''')
    st.dataframe(wallets, use_container_width=True)