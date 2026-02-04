import streamlit as st
from .dashboard_backend import get_admin_metrics

def render_admin_dashboard():
    st.markdown("<div class='sic-mart-header'>🎛️ Admin Dashboard</div>", unsafe_allow_html=True)
    
    metrics = get_admin_metrics()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Users", metrics['user_count'])
    c2.metric("Total Orders", metrics['order_count'])
    c3.metric("Escrow Pool", f"₹{metrics['escrow_sum']:,.2f}")

    st.markdown("---")
    st.success("✅ System operational. Dashboard logic connected to backend.")