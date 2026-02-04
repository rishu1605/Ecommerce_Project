import streamlit as st
import pandas as pd
# Using relative import as per your structure
from .wallet_backend import get_wallet_data, top_up_wallet

def render_wallet_ui(): # Renamed from render_buyer_wallet to match your main's import
    # Ensure we use the correct key from session_state
    buyer_id = st.session_state.user_data.get('user_id') or st.session_state.user_data.get('id')
    
    # Fetch data from backend
    balance, history = get_wallet_data(buyer_id)
    
    st.markdown("<div style='font-size: 24px; font-weight: bold; color: #0F52BA; margin-bottom: 20px;'>💎 Sapphire Wallet</div>", unsafe_allow_html=True)

    # 1. Balance Display (Glassmorphic Card)
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(15, 82, 186, 0.8), rgba(0, 0, 0, 0.9)); 
                    padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); text-align: center; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);'>
            <p style='color: #87CEEB; margin-bottom: 5px; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;'>Available Balance</p>
            <h1 style='color: white; font-size: 48px; margin-top: 0;'>₹{balance:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # 2. Quick Actions
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("💳 Top Up Wallet", expanded=False):
        amount = st.number_input("Enter Amount (₹)", min_value=100, step=500, key="topup_amt")
        if st.button("Add Funds", use_container_width=True):
            if top_up_wallet(buyer_id, amount):
                st.success(f"₹{amount} successfully added to your wallet!")
                st.rerun()
            else:
                st.error("Transaction failed. Please try again.")

    st.markdown("---")

    # 3. Transaction History
    st.markdown("#### 📜 Recent Activity")
    
    if history is None or history.empty:
        st.info("No transaction history found.")
    else:
        for _, row in history.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                
                # Logic for status visualization
                status_raw = str(row['status']).lower()
                if status_raw == 'refunded':
                    icon, label, color = "🎯", "Refund Received", "#00FF00"
                    prefix = "+"
                elif status_raw == 'escrow' or status_raw == 'pending':
                    icon, label, color = "🔒", "Payment in Escrow", "#FFD700"
                    prefix = "-"
                else:
                    icon, label, color = "🛒", "Purchase", "#FFFFFF"
                    prefix = "-"

                c1.write(f"{icon} **{label}**")
                # Handling date display
                date_val = row.get('created_at') or row.get('date') or "Recent"
                order_id = row.get('order_id') or "N/A"
                c1.caption(f"Order: #{order_id} | {date_val}")
                
                # Formatting amount
                amt = row.get('amount', 0)
                c2.write(f"**{prefix} ₹{amt:,.2f}**")
                
                c3.markdown(f"<p style='color: {color}; font-size: 12px; font-weight: bold; margin-top: 5px;'>{status_raw.upper()}</p>", unsafe_allow_html=True)
                st.markdown("<hr style='opacity: 0.1; margin: 10px 0;'>", unsafe_allow_html=True)