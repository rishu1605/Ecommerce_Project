import database as db
from common.status_codes import OrderStatus, PaymentStatus

def get_6_tile_metrics(seller_id):
    """Fetches data for the 6 dashboard tiles with synchronized logic."""
    
    # 1. Total Revenue (Released)
    rev = db.fetch_query("""
        SELECT SUM(amount) as val FROM payments p 
        JOIN orders o ON p.order_id = o.order_id 
        WHERE o.seller_id = ? AND p.status = ?
    """, (seller_id, PaymentStatus.RELEASED))
    
    # 2. Escrow Balance (Pending Payout)
    esc = db.fetch_query("""
        SELECT SUM(amount) as val FROM payments p 
        JOIN orders o ON p.order_id = o.order_id 
        WHERE o.seller_id = ? AND p.status = ?
    """, (seller_id, PaymentStatus.ESCROW))
    
    # 3. Active Shipments (In Transit)
    ship = db.fetch_query("""
        SELECT COUNT(*) as val FROM tracking t 
        JOIN orders o ON t.order_id = o.order_id 
        WHERE o.seller_id = ? AND t.current_status IN (?, ?)
    """, (seller_id, OrderStatus.SHIPPED, OrderStatus.OUT_FOR_DELIVERY))
    
    # 4. Live Products (Synchronized with Buyer View)
    # We add filters for 'active' and 'stock > 0' so this matches the Buyer's Dashboard
    prod = db.fetch_query("""
        SELECT COUNT(*) as val FROM products 
        WHERE seller_id = ? AND status = 'active' AND stock > 0 AND is_approved = 1
    """, (seller_id,))
    
    # 5. Pending Orders (New)
    pending = db.fetch_query("""
        SELECT COUNT(*) as val FROM orders 
        WHERE seller_id = ? AND order_id NOT IN (SELECT order_id FROM tracking)
    """, (seller_id,))
    
    # 6. Disputes/Returns
    dispute = db.fetch_query("""
        SELECT COUNT(*) as val FROM orders 
        WHERE seller_id = ? AND total_price < 0
    """, (seller_id,)) 

    return {
        "Revenue": rev.iloc[0]['val'] or 0,
        "Escrow": esc.iloc[0]['val'] or 0,
        "Active Shipments": ship.iloc[0]['val'] or 0,
        "Live Products": prod.iloc[0]['val'] or 0,
        "New Orders": pending.iloc[0]['val'] or 0,
        "Returns": dispute.iloc[0]['val'] or 0
    }