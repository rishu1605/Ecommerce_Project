import pandas as pd
import database as db
from datetime import datetime

def get_wallet_data(user_id):
    """
    Fetches the current balance and transaction history for a specific user.
    Ensures a wallet exists for the user before fetching.
    """
    try:
        # 1. ENSURE WALLET EXISTS (Safety First)
        # We check if a wallet exists; if not, we create it.
        check_query = "SELECT balance FROM wallets WHERE user_id = ?"
        balance_df = db.fetch_query(check_query, (user_id,))
        
        if balance_df.empty:
            db.execute_query("INSERT INTO wallets (user_id, balance) VALUES (?, 0.0)", (user_id,))
            balance = 0.0
        else:
            balance = float(balance_df.iloc[0]['balance'])

        # 2. Fetch Transaction History
        history_query = """
            SELECT amount, status, order_id, created_at 
            FROM transactions 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        """
        history = db.fetch_query(history_query, (user_id,))
        
        return balance, history

    except Exception as e:
        print(f"❌ Error fetching wallet data: {e}")
        return 0.0, pd.DataFrame()

def top_up_wallet(user_id, amount):
    """
    Updates the wallet balance and logs the transaction.
    Includes a debug print to capture exactly why a payment might fail.
    """
    if amount <= 0:
        return False

    try:
        # Step A: Double-check if wallet exists (prevents UPDATE failing on 0 rows)
        check_query = "SELECT 1 FROM wallets WHERE user_id = ?"
        exists = db.fetch_query(check_query, (user_id,))
        
        if exists.empty:
            db.execute_query("INSERT INTO wallets (user_id, balance) VALUES (?, 0.0)", (user_id,))

        # Step B: Update the balance
        update_balance_query = "UPDATE wallets SET balance = balance + ? WHERE user_id = ?"
        db.execute_query(update_balance_query, (amount, user_id))

        # Step C: Log the transaction
        log_transaction_query = """
            INSERT INTO transactions (user_id, amount, status, order_id, created_at) 
            VALUES (?, ?, ?, ?, ?)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute_query(log_transaction_query, (
            user_id, 
            float(amount), 
            'completed', 
            'TOPUP', 
            timestamp
        ))

        print(f"✅ Success: ₹{amount} added to User {user_id}")
        return True

    except Exception as e:
        # THIS PRINT IS CRITICAL: Look at your VS Code terminal to see the real error
        print(f"⚠️ DATABASE ERROR during top-up: {e}")
        return False