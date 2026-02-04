import database as db

def get_all_orders_for_admin():
    query = """
        SELECT o.order_id, b.name as buyer_name, s.name as seller_name, 
               o.product_name, o.amount, o.status, o.date 
        FROM orders o
        JOIN users b ON o.buyer_id = b.user_id
        JOIN users s ON o.seller_id = s.user_id
        ORDER BY o.date DESC
    """
    return db.fetch_query(query)

def update_order_status(order_id, new_status):
    db.execute_query("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))