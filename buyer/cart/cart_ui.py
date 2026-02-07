import streamlit as st
import database as db
import os
import pandas as pd
from buyer.cart.cart_backend import get_cart_items, remove_from_cart, get_cart_total, clear_cart

def render_cart_ui():
    st.title("🛒 Your Shopping Cart")
    user_id = st.session_state.user_data['user_id']
    cart_items = get_cart_items(user_id)
    
    if cart_items.empty:
        st.info("Your cart is empty.")
        return

    total_amt = get_cart_total(user_id)
    
    for _, item in cart_items.iterrows():
        with st.container(border=True):
            col_img, col_info, col_del = st.columns([1.2, 2.5, 0.5])
            with col_img:
                raw_img = item.get('image_url', "").split("|")[0]
                if raw_img and str(raw_img) != 'nan':
                    st.image(raw_img, use_container_width=True)
            with col_info:
                st.subheader(item['name'])
                st.write(f"**Price:** ₹{item['price']:,} | **Qty:** {item['quantity']}")
            with col_del:
                if st.button("❌", key=f"del_{item['cart_id']}"):
                    remove_from_cart(item['cart_id'])
                    st.rerun()

    st.markdown("---")
    process_checkout(total_amt, cart_items, user_id)

def render_buy_now_payment():
    st.title("⚡ Express Checkout")
    if st.button("⬅️ Back to Marketplace"):
        st.session_state.buy_now_active = False
        st.rerun()

    item = st.session_state.get("buy_now_item")
    user_id = st.session_state.user_data['user_id']

    if item:
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            with c1:
                img = item.get('image_url', "").split("|")[0]
                if img: st.image(img, use_container_width=True)
            with c2:
                st.subheader(item['name'])
                st.write(f"### **Total: ₹{item['price']:,}**")

        temp_df = pd.DataFrame([item])
        process_checkout(item['price'], temp_df, user_id)

def process_checkout(total_amt, items_df, user_id):
    st.write("### 💳 Payment Details")
    method = st.radio("Method:", ["👛 Sapphire Wallet", "📱 UPI", "💳 Card", "🏦 Net Banking", "💵 Cash on Delivery"], key="pay_method")

    with st.container(border=True):
        if method == "👛 Sapphire Wallet":
            wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
            bal = wallet['balance'][0] if not wallet.empty else 0
            st.info(f"Balance: ₹{bal:,}")
        elif method == "📱 UPI":
            st.text_input("UPI ID", placeholder="user@bank")
        elif method == "💳 Card":
            st.text_input("Card Number", max_chars=16)
            c1, c2 = st.columns(2)
            c1.text_input("Expiry (MM/YY)")
            c2.text_input("CVV", type="password")
        elif method == "🏦 Net Banking":
            st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis"])
        elif method == "💵 Cash on Delivery":
            st.write("Pay at your doorstep.")

    if st.button("Complete Payment", use_container_width=True, type="primary"):
        if method == "👛 Sapphire Wallet":
            wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
            bal = wallet['balance'][0] if not wallet.empty else 0
            if bal < total_amt:
                st.error("Low Balance!")
                return
            db.execute_query("UPDATE wallets SET balance = balance - ? WHERE user_id = ?", (total_amt, user_id))
        
        finalize_order(user_id, items_df)

def finalize_order(user_id, items_df):
    try:
        for _, item in items_df.iterrows():
            db.execute_query("INSERT INTO orders (buyer_id, product_name, amount, status) VALUES (?, ?, ?, 'Confirmed')",
                             (user_id, item['name'], item['price'] * item.get('quantity', 1)))
        st.session_state.buy_now_active = False
        if not st.session_state.get("buy_now_item"): clear_cart(user_id)
        st.success("🎉 Order Placed!")
        st.balloons()
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")