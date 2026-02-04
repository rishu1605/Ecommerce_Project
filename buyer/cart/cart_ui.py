import streamlit as st
import database as db

def render_cart_ui():
    st.title("🛒 Your Shopping Cart")
    
    if 'cart' not in st.session_state or len(st.session_state.cart) == 0:
        st.info("Your cart is empty.")
        return

    total_amt = sum(item['price'] for item in st.session_state.cart)
    
    # Display Cart Items
    for i, item in enumerate(st.session_state.cart):
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{item['name']}** - ₹{item['price']}")
        if col2.button("❌", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

    st.markdown("---")
    st.subheader(f"Total Amount: ₹{total_amt}")

    if st.button("Proceed to Checkout", use_container_width=True):
        process_checkout(total_amt)

def process_checkout(total_amt):
    user_id = st.session_state.user_data['user_id']
    
    # 1. Check Wallet Balance
    wallet = db.fetch_query("SELECT balance FROM wallets WHERE user_id=?", (user_id,))
    balance = wallet['balance'][0] if not wallet.empty else 0
    
    if balance < total_amt:
        st.error(f"Insufficient funds! You need ₹{total_amt - balance} more in your wallet.")
    else:
        try:
            # 2. Deduct from Buyer Wallet
            db.execute_query("UPDATE wallets SET balance = balance - ? WHERE user_id = ?", (total_amt, user_id))
            
            # 3. Create Orders & Update Seller Wallets
            for item in st.session_state.cart:
                # Add Order Record
                db.execute_query(
                    "INSERT INTO orders (buyer_id, seller_id, product_name, amount, status) VALUES (?, ?, ?, ?, 'Confirmed')",
                    (user_id, item['seller_id'], item['name'], item['price'])
                )
                # Credit Seller
                db.execute_query("UPDATE wallets SET balance = balance + ? WHERE user_id = ?", (item['price'], item['seller_id']))
                # Reduce Product Stock
                db.execute_query("UPDATE products SET stock = stock - 1 WHERE product_id = ?", (item['id'],))
            
            st.session_state.cart = [] # Clear Cart
            st.success("🎉 Order Placed Successfully!")
            st.balloons()
        except Exception as e:
            st.error(f"Transaction Failed: {e}")