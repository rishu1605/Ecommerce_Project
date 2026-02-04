import database as db

def get_marketplace_products(search_query=None):
    """Fetches products. Optionally filters by name or specs."""
    if search_query:
        return db.fetch_query("""
            SELECT p.*, s.store_name 
            FROM products p 
            JOIN seller_profiles s ON p.seller_id = s.seller_id
            WHERE p.name LIKE ? OR p.specs LIKE ?
        """, (f"%{search_query}%", f"%{search_query}%"))
    
    return db.fetch_query("""
        SELECT p.*, s.store_name 
        FROM products p 
        JOIN seller_profiles s ON p.seller_id = s.seller_id
    """)

def place_order(buyer_id, product_id, seller_id, amount):
    """
    1. Deducts amount from buyer wallet (logic added later in Wallet module).
    2. Creates the Order record.
    3. Initializes the Escrow Payment record.
    """
    order_id = f"ORD-{db.pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create Order
    db.execute_query("""
        INSERT INTO orders (order_id, buyer_id, seller_id, product_id, quantity, total_price)
        VALUES (?, ?, ?, ?, 1, ?)
    """, (order_id, buyer_id, seller_id, product_id, amount))
    
    # Create Escrow Payment (Locked until tracking confirms delivery)
    db.execute_query("""
        INSERT INTO payments (order_id, amount, commission, status)
        VALUES (?, ?, ?, 'escrow')
    """, (order_id, amount, amount * 0.10)) # Assuming 10% commission
    
    return order_id