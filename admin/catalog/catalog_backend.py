import database as db

def get_all_products_for_audit():
    """Fetches all listings with seller store names for oversight."""
    return db.fetch_query("""
        SELECT p.id, p.name, p.price, p.stock, p.status, s.store_name, p.seller_id
        FROM products p
        JOIN seller_profiles s ON p.seller_id = s.seller_id
        ORDER BY p.status ASC
    """)

def update_product_status(product_id, new_status):
    """
    Status options: 'Active', 'Flagged', 'Under Review'
    'Flagged' items are hidden from the Buyer's Home Marketplace.
    """
    db.execute_query("UPDATE products SET status = ? WHERE id = ?", (new_status, product_id))
    return True

def administrative_delete_product(product_id):
    """Permanent removal of a product violating terms."""
    db.execute_query("DELETE FROM products WHERE id = ?", (product_id,))
    return True