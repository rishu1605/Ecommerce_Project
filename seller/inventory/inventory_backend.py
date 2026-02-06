import database as db

def get_seller_products(seller_id):
    """Fetches all products owned by a specific seller, including their status."""
    query = "SELECT * FROM products WHERE seller_id = ?"
    return db.fetch_query(query, (seller_id,))

def add_product(seller_id, name, price, stock, desc, cat):
    """
    Adds a new product to the database.
    Explicitly sets 'status' to 'active' and 'is_approved' to 1 
    so the Buyer Dashboard can see it immediately.
    """
    # Note: Ensure these columns (status, is_approved) exist in your SQL table
    query = """
        INSERT INTO products (seller_id, name, price, stock, description, category, status, is_approved) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    # We set status='active' and is_approved=1 (True)
    # If your system requires Admin review first, set is_approved=0
    status = 'active'
    is_approved = 1 
    
    params = (seller_id, name, price, stock, desc, cat, status, is_approved)
    db.execute_query(query, params)

def update_stock(product_id, new_stock):
    """Updates the inventory count for an existing product."""
    query = "UPDATE products SET stock = ? WHERE product_id = ?"
    db.execute_query(query, (new_stock, product_id))

def toggle_product_status(product_id, status):
    """Allows a seller to hide/show a product manually (e.g., 'active' or 'hidden')."""
    query = "UPDATE products SET status = ? WHERE product_id = ?"
    db.execute_query(query, (status, product_id))

def delete_product(product_id, seller_id):
    """Removes a product from the shop."""
    query = "DELETE FROM products WHERE product_id = ? AND seller_id = ?"
    db.execute_query(query, (product_id, seller_id))