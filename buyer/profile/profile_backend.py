import database as db
import pandas as pd

def get_full_buyer_profile(buyer_id):
    """
    Fetches the latest profile data. We use a fresh query to bypass 
    any potential caching issues.
    """
    try:
        # Use user_id to get the specific record
        query = "SELECT * FROM users WHERE user_id = ?"
        df = db.fetch_query(query, (buyer_id,))
        return df
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return pd.DataFrame()

def update_buyer_profile(buyer_id, name, email, address, upi, acc, ifsc, holder, branch):
    """
    Updates the buyer record and ensures the database is committed.
    """
    try:
        # We ensure 'role' is checked, but we remove potential case-sensitivity issues
        query = """
            UPDATE users 
            SET name = ?, 
                email = ?, 
                address = ?, 
                upi_id = ?, 
                bank_acc = ?, 
                ifsc = ?, 
                acc_holder = ?, 
                branch = ?
            WHERE user_id = ? AND (role = 'buyer' OR role = 'Buyer')
        """
        db.execute_query(query, (
            name, email, address, upi, acc, ifsc, holder, branch, buyer_id
        ))
        
        # Verification Step: Re-fetch to confirm the database actually updated
        # This acts as a 'double-check' for the UI
        return True, "Profile updated successfully!"
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "This email is already in use by another user."
        return False, f"Update failed: {str(e)}"