import streamlit as st
import database as db
import pandas as pd

def render_admin_analytics():
    st.title("📈 Platform Analytics")
    
    # 1. User Growth
    user_counts = db.fetch_query("SELECT role, COUNT(*) as count FROM users GROUP BY role")
    
    # 2. Sales Trend
    sales_data = db.fetch_query("SELECT date, amount FROM orders")
    if not sales_data.empty:
        sales_data['date'] = pd.to_datetime(sales_data['date'])
        sales_trend = sales_data.set_index('date').resample('D').sum()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("User Distribution")
        st.bar_chart(user_counts.set_index('role'))
        
    with col2:
        st.subheader("Daily Sales Revenue")
        if not sales_data.empty:
            st.line_chart(sales_trend)
        else:
            st.info("No sales data to visualize yet.")