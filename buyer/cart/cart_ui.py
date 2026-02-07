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
            # Column ratios: Image, Info, and Delete
            col_img, col_info, col_del = st.columns([1.2, 2.5, 0.5])
            
            with col_img:
                # Extract the first image if multiple are stored (Logic from home_ui.py)
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
                        st.caption(f"Path: {img_path}")
                else:
                    st.write("🖼️ No Image")

            with col_info:
                st.subheader(item['name'])
                st.write(f"**Price:** ₹{item['price']:,} | **Quantity:** {item['quantity']}")
                st.write(f"**Subtotal:** ₹{item['price'] * item['quantity']:,}")

            with col_del:
                # Unique keys for each delete button
                if st.button("❌", key=f"del_{item['cart_id']}"):
                    remove_from_cart(item['cart_id'])
                    st.rerun()

    st.markdown("---")
    st.subheader(f"Total Amount: ₹{total_amt:,}")

    if st.button("Proceed to Checkout", use_container_width=True):
        process_checkout(total_amt, cart_items, user_id)

def process_checkout(total_amt, cart_items, user_id):
    """Handles the wallet deduction and order placement."""
    wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
    balance = wallet['balance'][0] if not wallet.empty else 0
    
    if balance < total_amt:
        st.error(f"Insufficient funds! Your balance is ₹{balance:,}")
    else:
        try:
            # Deduct Balance
            db.execute_query("UPDATE wallets SET balance = balance - ? WHERE user_id = ?", (total_amt, user_id))
            
            # Place Orders for each item
            for _, item in cart_items.iterrows():
                db.execute_query(
                    "INSERT INTO orders (buyer_id, product_name, amount, status) VALUES (?, ?, ?, 'Confirmed')",
                    (user_id, item['name'], item['price'] * item['quantity'])
                )
            
            clear_cart(user_id)
            st.success("🎉 Order Placed Successfully!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Transaction Failed: {e}")