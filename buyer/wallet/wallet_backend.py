import database as db
import pandas as pd

def get_wallet_data(buyer_id):
    """Fetches current balance from the wallets table and transaction history from orders."""
    
    # 1. Fetch Balance from the 'wallets' table (NOT users)
    balance_df = db.fetch_query("SELECT balance FROM wallets WHERE user_id = ?", (buyer_id,))
    
    if not balance_df.empty:
        balance = float(balance_df.iloc[0]['balance'])
    else:
        # If no wallet exists, create one with 0 balance
        db.execute_query("INSERT INTO wallets (user_id, balance) VALUES (?, 0.0)", (buyer_id,))
        balance = 0.0

    # 2. Fetch Transaction History
    # Note: We use the 'orders' table as the source of truth for transactions
    history = db.fetch_query("""
        SELECT order_id, amount, status, date as created_at 
        FROM orders 
        WHERE buyer_id = ?
        ORDER BY date DESC
    """, (buyer_id,))
    
    return balance, history

def top_up_wallet(buyer_id, amount):
    """Updates the balance in the wallets table."""
    try:
        # Check if wallet exists first
        check = db.fetch_query("SELECT user_id FROM wallets WHERE user_id = ?", (buyer_id,))
        
        if check.empty:
            db.execute_query("INSERT INTO wallets (user_id, balance) VALUES (?, ?)", (buyer_id, amount))
        else:
            db.execute_query("""
                UPDATE wallets SET balance = balance + ? 
                WHERE user_id = ?
            """, (amount, buyer_id))
        return True
    except Exception as e:
        print(f"Wallet Update Error: {e}")
        return False