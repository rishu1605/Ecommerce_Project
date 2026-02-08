import streamlit as st
import pandas as pd
import time
# Ensure your folder has an empty __init__.py for this relative import to work
from .wallet_backend import get_wallet_data, top_up_wallet

def render_wallet_ui():
    # 1. AESTHETIC CSS INJECTION
    st.markdown("""
        <style>
        /* Main Background */
        .stApp {
            background-color: #0f172a;
        }

        /* Hero Wallet Card */
        .wallet-card {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 25px;
        }

        .wallet-label {
            color: rgba(255,255,255,0.9);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }

        .wallet-balance-text {
            color: white !important;
            font-size: 52px;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        /* Payment Selection Box */
        .payment-box {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #334155;
            margin-top: 15px;
        }

        /* Section Headers */
        .section-header {
            color: #94a3b8;
            margin-top: 20px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. DATA INITIALIZATION
    # Safety check for user_id in session state
    if "user_data" not in st.session_state:
        st.error("User session not found. Please log in.")
        return

    user_data = st.session_state.user_data
    buyer_id = user_data.get('user_id') or user_data.get('id')
    
    # Fetch data from backend
    balance, history = get_wallet_data(buyer_id)
    
    st.markdown("<h2 style='color: white;'>💎 Sapphire Wallet</h2>", unsafe_allow_html=True)

    # 3. AMBER BALANCE DISPLAY
    st.markdown(f"""
        <div class="wallet-card">
            <div class="wallet-label">Available Balance</div>
            <h1 class="wallet-balance-text">₹{balance:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # 4. TOP UP SECTION
    with st.expander("➕ Add Funds to Wallet", expanded=False):
        amount = st.number_input("Amount (₹)", min_value=100, step=500, key="topup_amt_input")
        
        st.markdown("<p class='section-header'>Select Payment Method</p>", unsafe_allow_html=True)
        payment_mode = st.radio(
            "Method",
            ["UPI", "Credit/Debit Card", "Net Banking"],
            horizontal=True,
            label_visibility="collapsed"
        )

        # Conditional Input Fields
        st.markdown('<div class="payment-box">', unsafe_allow_html=True)
        if payment_mode == "UPI":
            st.markdown("<b style='color:white;'>📱 UPI Payment</b>", unsafe_allow_html=True)
            upi_id = st.text_input("UPI ID", placeholder="user@bankname")
            
        elif payment_mode == "Credit/Debit Card":
            st.markdown("<b style='color:white;'>💳 Card Details</b>", unsafe_allow_html=True)
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.text_input("Card Number", placeholder="0000 0000 0000 0000")
                st.text_input("Cardholder Name")
            with col_b:
                st.text_input("Expiry", placeholder="MM/YY")
                st.text_input("CVV", type="password", placeholder="***")
                
        elif payment_mode == "Net Banking":
            st.markdown("<b style='color:white;'>🏦 Select Bank</b>", unsafe_allow_html=True)
            st.selectbox("Choose Bank", ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("<br>", unsafe_allow_html=True)
        
        if st.button(f"Pay ₹{amount:,.2f} Now", use_container_width=True, type="primary"):
            if top_up_wallet(buyer_id, amount):
                st.success(f"Successfully added ₹{amount:,.2f}!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("Payment failed. Please try again.")

    st.markdown("---")

    # 5. TRANSACTION HISTORY
    st.markdown("<p class='section-header'>📜 Recent Activity</p>", unsafe_allow_html=True)
    
    if history is None or history.empty:
        st.info("No transactions yet.")
    else:
        for _, row in history.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                
                # Dynamic Styling based on Status
                status_raw = str(row['status']).lower()
                if status_raw == 'refunded':
                    icon, label, color, prefix = "🎯", "Refund", "#4ade80", "+"
                elif status_raw in ['escrow', 'pending']:
                    icon, label, color, prefix = "🔒", "Pending", "#facc15", "-"
                else:
                    icon, label, color, prefix = "🛒", "Payment", "#f8fafc", "-"

                with c1:
                    st.markdown(f"{icon} <b style='color: white;'>{label}</b>", unsafe_allow_html=True)
                    order_id = row.get('order_id') or "N/A"
                    date_val = row.get('created_at') or row.get('date') or "Today"
                    st.caption(f"Ref: #{order_id} | {date_val}")
                
                with c2:
                    amt = row.get('amount', 0)
                    st.markdown(f"<b style='color: white;'>{prefix} ₹{amt:,.2f}</b>", unsafe_allow_html=True)
                
                with c3:
                    st.markdown(f"<p style='color: {color}; font-size: 11px; font-weight: bold; margin-top: 5px;'>{status_raw.upper()}</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='border: 0.1px solid #334155; margin: 10px 0;'>", unsafe_allow_html=True)