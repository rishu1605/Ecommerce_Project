import database as db

def get_seller_orders(seller_id):
    """
    Fetches orders for a specific seller.
    Uses CAST to prevent type mismatches and LEFT JOIN to prevent blank screens.
    """
    # Force seller_id to string to match CAST in SQL
    s_id = str(seller_id)
    
    query = """
        SELECT 
            o.order_id, 
            o.product_name, 
            o.amount, 
            o.status, 
            o.date, 
            o.shipping_address,
            COALESCE(u.name, 'Buyer ID: ' || o.buyer_id) as customer_name
        FROM orders o
        LEFT JOIN users u ON CAST(o.buyer_id AS TEXT) = CAST(u.user_id AS TEXT)
        WHERE CAST(o.seller_id AS TEXT) = ?
        ORDER BY o.date DESC
    """
    return db.fetch_query(query, (s_id,))

def update_order_status(order_id, new_status):
    """Updates the status of a specific order in the database."""
    query = "UPDATE orders SET status = ? WHERE order_id = ?"
    return db.execute_query(query, (new_status, order_id))