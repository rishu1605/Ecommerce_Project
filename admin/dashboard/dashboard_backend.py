import database as db

def get_admin_metrics():
    """Fetches key performance indicators for the admin dashboard."""
    metrics = {}
    try:
        metrics['user_count'] = db.fetch_query("SELECT COUNT(*) as count FROM users")['count'][0]
        metrics['order_count'] = db.fetch_query("SELECT COUNT(*) as count FROM orders")['count'][0]
        
        escrow_data = db.fetch_query("SELECT SUM(amount) as total FROM payments WHERE status='escrow'")
        metrics['escrow_sum'] = escrow_data['total'][0] if escrow_data['total'][0] else 0
    except Exception:
        metrics = {'user_count': 0, 'order_count': 0, 'escrow_sum': 0}
    return metrics