import database as db
import pandas as pd

def get_marketplace_products(search_query=None):
    """
    Fetches products that are in stock.
    Uses LEFT JOIN so products appear even if seller profile is missing.
    """

    # Only filter we can safely apply based on current DB schema
    market_filters = "WHERE p.stock > 0"

    if search_query:
        query = """
            SELECT 
                p.*, 
                COALESCE(s.store_name, 'Independent Seller') AS store_name
            FROM products p
            LEFT JOIN seller_profiles s 
                ON p.seller_id = s.seller_id
            WHERE p.stock > 0
              AND (
                    p.name LIKE ? 
                 OR p.description LIKE ? 
                 OR p.category LIKE ?
              )
        """
        params = (
            f"%{search_query}%",
            f"%{search_query}%",
            f"%{search_query}%"
        )
        return db.fetch_query(query, params)

    # Default marketplace view (no search)
    query = f"""
        SELECT 
            p.*, 
            COALESCE(s.store_name, 'Independent Seller') AS store_name
        FROM products p
        LEFT JOIN seller_profiles s 
            ON p.seller_id = s.seller_id
        {market_filters}
    """
    return db.fetch_query(query)


def place_order(buyer_id, product_id, seller_id, amount):
    """Handles order creation and payment record creation."""

    # Generate Order ID
    order_id = f"ORD-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

    # Insert order
    db.execute_query("""
        INSERT INTO orders (buyer_id, seller_id, product_name, amount)
        VALUES (?, ?, ?, ?)
    """, (buyer_id, seller_id, product_id, amount))

    # Insert payment (simple version based on your schema)
    db.execute_query("""
        INSERT INTO payments (order_id, user_id, amount, type, status)
        VALUES (?, ?, ?, 'escrow', 'pending')
    """, (order_id, buyer_id, amount))

    return order_id
