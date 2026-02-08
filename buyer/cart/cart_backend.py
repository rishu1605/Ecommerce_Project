import database as db
import streamlit as st

def add_to_cart(product_id, user_id):
    """Adds a product to the cart or increments quantity if already present."""
    # Ensure IDs are integers for database consistency
    try:
        p_id = int(product_id)
        u_id = int(user_id)
    except (ValueError, TypeError):
        st.error("Invalid Product or User ID.")
        return

    # DEBUG: Terminal log
    print(f"DEBUG: Attempting to add Product ID: {p_id} for User ID: {u_id}")

    if not u_id:
        st.error("User session expired. Please log in again.")
        return

    # Check if product already exists in this user's cart
    existing = db.fetch_query(
        "SELECT * FROM cart WHERE buyer_id = ? AND product_id = ?", 
        (u_id, p_id)
    )
    
    if existing is not None and not existing.empty:
        # Increment quantity
        db.execute_query(
            "UPDATE cart SET quantity = quantity + 1 WHERE buyer_id = ? AND product_id = ?",
            (u_id, p_id)
        )
        print("DEBUG: Incremented existing item quantity.")
    else:
        # Insert new record
        db.execute_query(
            "INSERT INTO cart (buyer_id, product_id, quantity) VALUES (?, ?, ?)",
            (u_id, p_id, 1)
        )
        print("DEBUG: Inserted new item into cart.")
    
    st.toast("🛒 Added to cart!")

def get_cart_items(user_id):
    """Retrieves all items in the cart for a specific user with product details."""
    try:
        u_id = int(user_id)
    except (ValueError, TypeError):
        return None

    # Using LEFT JOIN to ensure cart records show up even if product details are tricky
    query = """
        SELECT c.cart_id, c.quantity, p.name, p.price, p.product_id, p.description, p.image_url 
        FROM cart c 
        LEFT JOIN products p ON c.product_id = p.product_id 
        WHERE c.buyer_id = ?
    """
    df = db.fetch_query(query, (u_id,))
    
    # DEBUG: Monitor retrieval
    if df is not None:
        print(f"DEBUG: Retrieved {len(df)} items for User {u_id}")
    return df

def remove_from_cart(cart_id):
    """Removes a specific entry from the cart by its unique cart_id."""
    db.execute_query("DELETE FROM cart WHERE cart_id = ?", (cart_id,))

def clear_cart(user_id):
    """Wipes the entire cart for a specific user."""
    db.execute_query("DELETE FROM cart WHERE buyer_id = ?", (user_id,))

def get_cart_total(user_id):
    """Calculates the subtotal for all items in the cart."""
    items = get_cart_items(user_id)
    if items is None or items.empty:
        return 0.0
    # Ensure price and quantity are numeric before summing
    return (items['price'] * items['quantity']).sum()