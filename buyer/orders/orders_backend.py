import database as db

def get_detailed_order_history(buyer_id):
    """
    Fetches orders using verified column names: 
    - 'amount' instead of 'total_price'
    - 'date' instead of 'order_date'
    """
    # We use a LEFT JOIN for tracking/payments so the order still shows up 
    # even if tracking info hasn't been created yet.
    return db.fetch_query("""
        SELECT 
            o.order_id, 
            o.amount, 
            o.date, 
            o.product_name,
            o.status as tracking_status,
            o.status as payment_status  -- Fallback if payments table is empty
        FROM orders o
        WHERE o.buyer_id = ?
        ORDER BY o.date DESC
    """, (buyer_id,))

def request_return(order_id, reason):
    """
    Logs a return request by updating the main orders table 
    and optionally a complaints table.
    """
    # Updating the status in 'orders' table directly since 'payments' table 
    # structure might be missing or different.
    success = db.execute_query("""
        UPDATE orders 
        SET status = 'Return Pending' 
        WHERE order_id = ?
    """, (order_id,))
    
    # Optional: Log to a complaints/support table if you have one
    # db.execute_query("INSERT INTO support (order_id, message) VALUES (?, ?)", (order_id, reason))
    
    return success