import database as db

def get_buyer_orders(buyer_id):
    """Fetches orders so the buyer can link the complaint to a specific purchase."""
    return db.fetch_query("""
        SELECT o.order_id, p.name 
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        WHERE o.buyer_id = ?
    """, (buyer_id,))

def submit_complaint(buyer_id, order_id, subject, description):
    """Logs the issue and automatically finds the associated seller_id."""
    # Retrieve seller_id from the order record
    order_info = db.fetch_query("SELECT seller_id FROM orders WHERE order_id = ?", (order_id,))
    if order_info.empty:
        return False, "Order not found."
    
    seller_id = order_info.iloc[0]['seller_id']
    
    db.execute_query("""
        INSERT INTO complaints (order_id, buyer_id, seller_id, subject, description) 
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, buyer_id, seller_id, subject, description))
    
    return True, "Ticket Raised Successfully. An Admin will review it shortly."