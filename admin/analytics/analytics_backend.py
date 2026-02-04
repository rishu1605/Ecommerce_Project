import database as db
import pandas as pd

def get_detailed_analytics():
    """Aggregates data for charts and growth tracking."""
    # 1. Sales Trend (Last 7 Days)
    sales_trend = db.fetch_query("""
        SELECT DATE(created_at) as date, SUM(amount) as daily_total 
        FROM payments 
        WHERE status = 'released' 
        GROUP BY DATE(created_at) 
        ORDER BY date DESC LIMIT 7
    """)

    # 2. Category Distribution
    category_data = db.fetch_query("""
        SELECT p.specs as category, COUNT(o.order_id) as volume 
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        GROUP BY p.specs
    """)

    # 3. Escrow Health
    escrow_stats = db.fetch_query("""
        SELECT status, SUM(amount) as total 
        FROM payments 
        GROUP BY status
    """)
    
    return sales_trend, category_data, escrow_stats