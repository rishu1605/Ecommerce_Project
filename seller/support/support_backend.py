import database as db

def get_forwarded_complaints(seller_id):
    """
    Fetches complaints that the Admin has reviewed and 
    marked as 'Forwarded' to the seller.
    """
    return db.fetch_query("""
        SELECT c.id, c.order_id, c.subject, c.message, c.created_at, u.name as buyer_name
        FROM complaints c
        JOIN orders o ON c.order_id = o.order_id
        JOIN users u ON o.buyer_id = u.id
        WHERE o.seller_id = ? AND c.status = 'Forwarded'
    """, (seller_id,))

def resolve_complaint(complaint_id, resolution_text):
    """Updates the complaint status and logs the seller's response."""
    db.execute_query("""
        UPDATE complaints 
        SET status = 'Resolved', resolution = ?, resolved_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (resolution_text, complaint_id))
    return True