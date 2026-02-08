import database as db
from common.status_codes import OrderStatus, PaymentStatus

def get_6_tile_metrics(seller_id):
    """Fetches data for the 6 dashboard tiles with corrected column names."""
    try:
        # 1. Total Revenue (Released)
        rev = db.fetch_query("""
            SELECT SUM(amount) as val FROM orders 
            WHERE seller_id = ? AND status = 'Delivered'
        """, (seller_id,))
        
        # 2. Escrow Balance (Pending Payout)
        esc = db.fetch_query("""
            SELECT SUM(amount) as val FROM orders 
            WHERE seller_id = ? AND status IN ('Confirmed', 'Shipped')
        """, (seller_id,))
        
        # 3. Active Shipments
        ship = db.fetch_query("""
            SELECT COUNT(*) as val FROM orders 
            WHERE seller_id = ? AND status = 'Shipped'
        """, (seller_id,))
        
        # 4. Live Products (Corrected 'product_id' vs 'id' logic)
        prod = db.fetch_query("""
            SELECT COUNT(*) as val FROM products 
            WHERE seller_id = ? AND stock > 0
        """, (seller_id,))
        
        # 5. New Orders (FIX: Counts 'Confirmed' orders that need processing)
        pending = db.fetch_query("""
            SELECT COUNT(*) as val FROM orders 
            WHERE seller_id = ? AND status = 'Confirmed'
        """, (seller_id,))
        
        # 6. Returns
        dispute = db.fetch_query("""
            SELECT COUNT(*) as val FROM orders 
            WHERE seller_id = ? AND status = 'Returned'
        """, (seller_id,))

        return {
            "Revenue": rev.iloc[0]['val'] or 0.0,
            "Escrow": esc.iloc[0]['val'] or 0.0,
            "Shipments": ship.iloc[0]['val'] or 0,
            "Live Products": prod.iloc[0]['val'] or 0,
            "New Orders": pending.iloc[0]['val'] or 0,
            "Returns": dispute.iloc[0]['val'] or 0
        }
    except Exception as e:
        print(f"Dashboard Error: {e}")
        return {"Revenue": 0.0, "Escrow": 0.0, "Shipments": 0, "Live Products": 0, "New Orders": 0, "Returns": 0}