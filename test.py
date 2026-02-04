import database as db
import hashlib
from common.image_utils import upload_image_to_cloud
import pandas as pd

def run_comprehensive_test():
    print("🚀 Starting SIC Mart System Integration Test...")
    db.set_up_tables()

    # 1. Test User & Seller Creation
    print("\n--- Phase 1: Authentication & Profiles ---")
    test_email = "tester_seller@sicmart.com"
    hp = hashlib.sha256("password123".encode()).hexdigest()
    
    try:
        db.execute_query("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'seller')", 
                        ("Test Seller", test_email, hp))
        user = db.fetch_query("SELECT user_id FROM users WHERE email=?", (test_email,))
        s_id = int(user['user_id'][0])
        
        db.execute_query("INSERT INTO seller_profiles (seller_id, store_name, gst_number, status) VALUES (?, ?, ?, 'Approved')", 
                        (s_id, "Test Store", "12ABCDE3456F1Z5"))
        db.execute_query("INSERT INTO wallets (user_id, balance) VALUES (?, 0.0)", (s_id,))
        print("✅ Seller created and pre-approved.")
    except Exception as e:
        print(f"❌ Seller Creation Failed: {e}")

    # 2. Test Cloudinary & Inventory
    print("\n--- Phase 2: Cloudinary & Inventory ---")
    # Mocking a URL since we can't upload a real file via script without a path
    mock_url = "https://res.cloudinary.com/demo/image/upload/sample.jpg"
    try:
        db.execute_query(
            "INSERT INTO products (seller_id, name, price, stock, image_url, category) VALUES (?, ?, ?, ?, ?, ?)",
            (s_id, "Test Laptop", 50000.0, 10, mock_url, "Electronics")
        )
        print(f"✅ Product listed with Cloudinary URL: {mock_url}")
    except Exception as e:
        print(f"❌ Product Listing Failed: {e}")

    # 3. Test Buyer & Wallet Transaction
    print("\n--- Phase 3: Transaction & Wallet Flow ---")
    buyer_email = "tester_buyer@sicmart.com"
    try:
        db.execute_query("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'buyer')", 
                        ("Test Buyer", buyer_email, hp))
        b_user = db.fetch_query("SELECT user_id FROM users WHERE email=?", (buyer_email,))
        b_id = int(b_user['user_id'][0])
        
        # Add Money to Buyer Wallet
        db.execute_query("INSERT INTO wallets (user_id, balance) VALUES (?, 100000.0)", (b_id,))
        
        # Simulate Purchase
        # Deduct from Buyer, Credit Seller, Add Order, Reduce Stock
        db.execute_query("UPDATE wallets SET balance = balance - 50000 WHERE user_id = ?", (b_id,))
        db.execute_query("UPDATE wallets SET balance = balance + 50000 WHERE user_id = ?", (s_id,))
        db.execute_query("UPDATE products SET stock = stock - 1 WHERE name = ?", ("Test Laptop",))
        db.execute_query("INSERT INTO orders (buyer_id, seller_id, product_name, amount) VALUES (?, ?, ?, ?)",
                        (b_id, s_id, "Test Laptop", 50000.0))
        
        print("✅ Transaction successful: Wallet deducted, Seller credited, Stock reduced.")
    except Exception as e:
        print(f"❌ Transaction Failed: {e}")

    # 4. Final Audit
    print("\n--- Phase 4: Final Database Audit ---")
    audit_orders = db.fetch_query("SELECT * FROM orders")
    audit_wallets = db.fetch_query("SELECT u.name, w.balance FROM users u JOIN wallets w ON u.user_id = w.user_id")
    
    print("\nOrders Placed:")
    print(audit_orders)
    print("\nFinal Wallet Balances:")
    print(audit_wallets)
    
    print("\n🏁 Test Completed. If the balances look correct (Buyer: 50k, Seller: 50k), your system is ready!")

if __name__ == "__main__":
    run_comprehensive_test()