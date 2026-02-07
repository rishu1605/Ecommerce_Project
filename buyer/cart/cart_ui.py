import streamlit as st
import database as db
import os
from buyer.cart.cart_backend import get_cart_items, remove_from_cart, get_cart_total, clear_cart

def render_cart_ui():
    st.title("🛒 Your Shopping Cart")
    
    if 'user_data' not in st.session_state:
        st.error("Please log in to view your cart.")
        return

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
                raw_image_data = item.get('image_url', "")
                url_list = raw_image_data.split("|") if raw_image_data else []
                img_path = url_list[0] if url_list else None
                
                if img_path and str(img_path) != 'nan':
                    if str(img_path).startswith(('http://', 'https://')):
                        st.image(img_path, use_container_width=True)
                    elif os.path.exists(str(img_path)):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.warning("⚠️ Image Missing")
                else:
                    st.write("🖼️ No Image")

            with col_info:
                st.subheader(item['name'])
                st.write(f"**Price:** ₹{item['price']:,} | **Quantity:** {item['quantity']}")
                st.write(f"**Subtotal:** ₹{item['price'] * item['quantity']:,}")

            with col_del:
                if st.button("❌", key=f"del_{item['cart_id']}"):
                    remove_from_cart(item['cart_id'])
                    st.rerun()

    st.markdown("---")
    st.subheader(f"Total Amount: ₹{total_amt:,}")

    # Trigger the multi-option checkout
    process_checkout(total_amt, cart_items, user_id)

def process_checkout(total_amt, cart_items, user_id):
    """Handles multi-option payment selection and order placement."""
    st.write("### 💳 Select Payment Method")
    
    with st.container(border=True):
        payment_method = st.radio(
            "Choose your preferred gateway:",
            ["👛 Sapphire Wallet", "📱 UPI (GPay/PhonePe)", "💳 Debit/Credit Card", "🏦 Net Banking"],
            index=0
        )

        st.divider()

        # Dynamic UI based on selection
        if payment_method == "👛 Sapphire Wallet":
            wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
            balance = wallet['balance'][0] if not wallet.empty else 0
            st.info(f"Wallet Balance: ₹{balance:,}")
            if balance < total_amt:
                st.warning("Insufficient funds in your wallet.")

        elif payment_method == "📱 UPI (GPay/PhonePe)":
            st.text_input("Enter Virtual Private Address (VPA)", placeholder="username@bank")
            st.caption("Standard UPI checkout will be triggered.")

        elif payment_method == "💳 Debit/Credit Card":
            st.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
            c1, c2 = st.columns(2)
            c1.text_input("Expiry", placeholder="MM/YY")
            c2.text_input("CVV", type="password", placeholder="***")

        elif payment_method == "🏦 Net Banking":
            st.selectbox("Choose your Bank", ["SBI", "HDFC", "ICICI", "Axis", "Kotak"])

    if st.button("Complete Payment", use_container_width=True, type="primary"):
        if payment_method == "👛 Sapphire Wallet":
            wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
            balance = wallet['balance'][0] if not wallet.empty else 0
            
            if balance < total_amt:
                st.error(f"Transaction Failed: Low Balance (₹{balance:,})")
            else:
                db.execute_query("UPDATE wallets SET balance = balance - ? WHERE user_id = ?", (total_amt, user_id))
                finalize_order(user_id, cart_items)
        else:
            # Simulate external gateway redirect
            st.toast(f"Redirecting to {payment_method} Gateway...")
            finalize_order(user_id, cart_items)

def finalize_order(user_id, cart_items):
    """Refactored logic to save orders and clear the cart."""
    try:
        for _, item in cart_items.iterrows():
            db.execute_query(
                "INSERT INTO orders (buyer_id, product_name, amount, status) VALUES (?, ?, ?, 'Confirmed')",
                (user_id, item['name'], item['price'] * item['quantity'])
            )
        
        clear_cart(user_id)
        st.success("🎉 Payment Successful! Your order is confirmed.")
        st.balloons()
        st.rerun()
    except Exception as e:
        st.error(f"Order Placement Error: {e}")