import streamlit as st
import database as db
import os
import time
import pandas as pd
from datetime import datetime
from buyer.cart.cart_backend import get_cart_items, remove_from_cart, get_cart_total, clear_cart

def render_cart_ui():
    st.markdown("<h2 style='color: white;'>🛒 Your Shopping Cart</h2>", unsafe_allow_html=True)
    user_id = st.session_state.user_data['user_id']
    cart_items = get_cart_items(user_id)
    
    if cart_items.empty:
        st.info("Your cart is empty.")
        return

    col_main, col_summary = st.columns([2, 1.3], gap="large")

    with col_main:
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

    with col_summary:
        render_price_summary(user_id, cart_items)

def render_buy_now_payment():
    st.title("⚡ Express Checkout")
    if st.button("⬅️ Back to Marketplace"):
        st.session_state.buy_now_active = False
        st.rerun()

    item = st.session_state.get("buy_now_item")
    user_id = st.session_state.user_data['user_id']

    if item:
        temp_df = pd.DataFrame([item])
        if 'quantity' not in temp_df.columns:
            temp_df['quantity'] = 1
            
        col_main, col_summary = st.columns([2, 1.3], gap="large")
        with col_main:
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    img = item.get('image_url', "").split("|")[0]
                    if img: st.image(img, use_container_width=True)
                with c2:
                    st.subheader(item['name'])
                    st.write(f"Unit Price: ₹{item['price']:,}")
        
        with col_summary:
            render_price_summary(user_id, temp_df, is_buy_now=True)

def render_price_summary(user_id, items_df, is_buy_now=False):
    subtotal = (items_df['price'] * items_df.get('quantity', 1)).sum()
    
    tax_rate = 0.18
    gst_amt = subtotal * tax_rate
    platform_fee = 20.0
    delivery_fee = 0.0 if subtotal > 1000 else 50.0
    final_total = subtotal + gst_amt + platform_fee + delivery_fee

    st.markdown("""
        <style>
        .price-card {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #334155;
        }
        .total-font {
            font-size: 22px;
            color: #f59e0b;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="price-card">', unsafe_allow_html=True)
        st.markdown("### Price Details")
        st.write(f"Subtotal: ₹{subtotal:,.2f}")
        st.write(f"GST (18%): ₹{gst_amt:,.2f}")
        st.write(f"Platform Fee: ₹{platform_fee:,.2f}")
        st.write(f"Delivery: {':green[FREE]' if delivery_fee == 0 else f'₹{delivery_fee:,.2f}'}")
        st.markdown("---")
        st.markdown(f'<div class="total-font">Total Payable: ₹{final_total:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    process_checkout(final_total, items_df, user_id)

def process_checkout(total_amt, items_df, user_id):
    # --- MULTI-ADDRESS SECTION ---
    st.write("### 📍 Shipping Address")
    
    # 1. Fetch all addresses from the new 'addresses' table
    saved_addr_df = db.fetch_query("SELECT * FROM addresses WHERE user_id = ?", (user_id,))
    
    # 2. Add Profile Address as an option if it exists
    user_prof = db.fetch_query("SELECT address FROM users WHERE user_id = ?", (user_id,))
    prof_addr = user_prof['address'][0] if not user_prof.empty else None

    addr_options = []
    addr_map = {}

    if prof_addr and str(prof_addr) != 'None' and prof_addr.strip() != "":
        label = "🏠 Profile Address"
        addr_options.append(label)
        addr_map[label] = prof_addr

    for _, row in saved_addr_df.iterrows():
        label = f"📍 {row['label']}: {row['address_text'][:30]}..."
        addr_options.append(label)
        addr_map[label] = row['address_text']

    addr_options.append("➕ Add New Address")
    
    selected_label = st.radio("Deliver to:", addr_options, horizontal=False)
    final_address = ""

    if selected_label == "➕ Add New Address":
        col1, col2 = st.columns([1, 2])
        new_label = col1.selectbox("Type", ["Home", "Work", "Other", "Friend"])
        new_addr = st.text_area("Full Address Details", placeholder="House/Flat No, Landmark, City, Pincode...")
        save_this = st.checkbox("Save this address for future checkouts")
        
        if new_addr.strip():
            final_address = new_addr
            # Note: We save to DB during finalize_order to ensure intent
    else:
        final_address = addr_map[selected_label]
        st.success(f"Selected: {final_address}")

    if not final_address:
        st.error("Please provide or select a shipping address.")
        return

    st.write("---")
    
    # --- PAYMENT SECTION ---
    st.write("### 💳 Payment Method")
    method = st.radio("Choose Method:", ["👛 Sapphire Wallet", "📱 UPI", "💳 Card", "💵 Cash on Delivery"], key="pay_method")

    with st.container(border=True):
        if method == "👛 Sapphire Wallet":
            wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
            bal = wallet['balance'][0] if not wallet.empty else 0
            if bal >= total_amt:
                st.info(f"Wallet Balance: ₹{bal:,.2f}")
            else:
                st.error(f"Low Balance! Need ₹{total_amt - bal:,.2f} more.")
        elif method == "💵 Cash on Delivery":
            st.warning("Pay ₹{total_amt:,.2f} at the time of delivery.")

    if st.button("Place Order", use_container_width=True, type="primary"):
        # Wallet logic
        if method == "👛 Sapphire Wallet":
            wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
            bal = wallet['balance'][0] if not wallet.empty else 0
            if bal < total_amt:
                st.error("Transaction failed: Insufficient balance.")
                return
            db.execute_query("UPDATE wallets SET balance = balance - ? WHERE user_id = ?", (total_amt, user_id))
        
        # Save new address if requested
        if selected_label == "➕ Add New Address" and save_this:
            db.execute_query(
                "INSERT INTO addresses (user_id, label, address_text) VALUES (?, ?, ?)",
                (user_id, new_label, new_addr)
            )

        finalize_order(user_id, items_df, total_amt, final_address)

def finalize_order(user_id, items_df, final_total, address):
    try:
        # Use the finalized shipping address for every item in this order
        for _, item in items_df.iterrows():
            db.execute_query(
                """INSERT INTO orders (buyer_id, product_name, amount, shipping_address, status, date) 
                   VALUES (?, ?, ?, ?, 'Confirmed', ?)""",
                (user_id, item['name'], item['price'] * item.get('quantity', 1), address, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            
        st.session_state.buy_now_active = False
        if not st.session_state.get("buy_now_item"): 
            clear_cart(user_id)
        else:
            st.session_state.buy_now_item = None
            
        st.success(f"🎉 Order of ₹{final_total:,.2f} confirmed!")
        st.balloons()
        time.sleep(2)
        st.rerun()
    except Exception as e:
        st.error(f"Error finalizing order: {e}")