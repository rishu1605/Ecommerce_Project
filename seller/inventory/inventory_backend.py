import database as db

def get_seller_products(seller_id):
    """Fetches all products owned by a specific seller."""
    query = "SELECT * FROM products WHERE seller_id = ?"
    return db.fetch_query(query, (seller_id,))

def add_product(seller_id, name, price, stock, desc, cat):
    """Adds a new product to the database."""
    query = """
        INSERT INTO products (seller_id, name, price, stock, description, category) 
        VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute_query(query, (seller_id, name, price, stock, desc, cat))

def update_stock(product_id, new_stock):
    """Updates the inventory count for an existing product."""
    query = "UPDATE products SET stock = ? WHERE product_id = ?"
    db.execute_query(query, (new_stock, product_id))

def delete_product(product_id, seller_id):
    """Removes a product from the shop."""
    query = "DELETE FROM products WHERE product_id = ? AND seller_id = ?"
    db.execute_query(query, (product_id, seller_id))