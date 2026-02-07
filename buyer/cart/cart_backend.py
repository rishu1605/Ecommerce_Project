import database as db
import streamlit as st

def add_to_cart(product_id, buyer_id):
    """Saves the product to the database or increments quantity."""
    existing = db.fetch_query(
        "SELECT * FROM cart WHERE buyer_id = ? AND product_id = ?", 
        (buyer_id, product_id)
    )
    
    if not existing.empty:
        db.execute_query(
            "UPDATE cart SET quantity = quantity + 1 WHERE buyer_id = ? AND product_id = ?",
            (buyer_id, product_id)
        )
    else:
        db.execute_query(
            "INSERT INTO cart (buyer_id, product_id, quantity) VALUES (?, ?, ?)",
            (buyer_id, product_id, 1)
        )
    st.toast("🛒 Added to cart!")

def get_cart_items(buyer_id):
    """Gets cart items with an explicit alias for the image path."""
    query = """
        SELECT 
            c.cart_id, 
            c.quantity, 
            p.name, 
            p.price, 
            p.product_id, 
            p.description, 
            p.image_url AS image_url 
        FROM cart c 
        JOIN products p ON c.product_id = p.product_id 
        WHERE c.buyer_id = ?
    """
    return db.fetch_query(query, (buyer_id,))

def remove_from_cart(cart_id):
    """Removes a specific row from the cart."""
    db.execute_query("DELETE FROM cart WHERE cart_id = ?", (cart_id,))

def clear_cart(buyer_id):
    """Removes all items for a user after checkout."""
    db.execute_query("DELETE FROM cart WHERE buyer_id = ?", (buyer_id,))

def get_cart_total(buyer_id):
    """Calculates total price from database items."""
    items = get_cart_items(buyer_id)
    if items.empty:
        return 0.0
    return (items['price'] * items['quantity']).sum()