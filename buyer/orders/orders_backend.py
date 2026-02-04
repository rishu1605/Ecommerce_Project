import database as db

def get_detailed_order_history(buyer_id):
    """Fetches orders with tracking, escrow status, and return updates."""
    return db.fetch_query("""
        SELECT 
            o.order_id, o.total_price, o.order_date, 
            p.name as product_name,
            t.current_status as tracking_status,
            pay.status as payment_status,
            pay.amount as refund_amount
        FROM orders o
        JOIN products p ON o.product_id = p.id
        LEFT JOIN tracking t ON o.order_id = t.order_id
        LEFT JOIN payments pay ON o.order_id = pay.order_id
        WHERE o.buyer_id = ?
        ORDER BY o.order_date DESC
    """, (buyer_id,))

def request_return(order_id, reason):
    """Logs a return request for the Admin to review."""
    # This status 'return_pending' alerts the Admin in their dashboard
    db.execute_query("""
        UPDATE payments SET status = 'return_pending' 
        WHERE order_id = ?
    """, (order_id,))
    # Log the reason in a support/complaints table
    return True