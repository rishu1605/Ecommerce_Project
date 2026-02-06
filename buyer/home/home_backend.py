import database as db
import pandas as pd

def get_marketplace_products(search_query=None):
    """
    Fetches products with stock > 0. 
    Uses LEFT JOIN to ensure products show even if seller_profile isn't fully set.
    """
    if search_query:
        query = """
            SELECT p.*, COALESCE(s.store_name, 'Independent Seller') as store_name 
            FROM products p 
            LEFT JOIN seller_profiles s ON p.seller_id = s.seller_id
            WHERE p.stock > 0 AND (p.name LIKE ? OR p.description LIKE ? OR p.category LIKE ?)
        """
        params = (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%")
        return db.fetch_query(query, params)
    
    query = """
        SELECT p.*, COALESCE(s.store_name, 'Independent Seller') as store_name 
        FROM products p 
        LEFT JOIN seller_profiles s ON p.seller_id = s.seller_id
        WHERE p.stock > 0
    """
    return db.fetch_query(query)

def place_order(buyer_id, product_id, seller_id, amount):
    """Handles order creation and Escrow initialization."""
    order_id = f"ORD-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create Order
    db.execute_query("""
        INSERT INTO orders (order_id, buyer_id, seller_id, product_id, quantity, total_price)
        VALUES (?, ?, ?, ?, 1, ?)
    """, (order_id, buyer_id, seller_id, product_id, amount))
    
    # Create Escrow Payment (10% platform commission)
    db.execute_query("""
        INSERT INTO payments (order_id, amount, commission, status)
        VALUES (?, ?, ?, 'escrow')
    """, (order_id, amount, amount * 0.10))
    
    return order_id