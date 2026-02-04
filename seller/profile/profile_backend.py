import database as db

def get_full_seller_profile(seller_id):
    """Fetches combined data from users and seller_profiles tables."""
    return db.fetch_query("""
        SELECT u.name, u.id, s.store_name, s.email, s.pan, 
               s.bank_acc, s.ifsc, s.branch, s.acc_holder
        FROM users u
        JOIN seller_profiles s ON u.id = s.seller_id
        WHERE u.id = ?
    """, (seller_id,))

def update_seller_profile(seller_id, name, store_name, email, bank_acc, ifsc, branch, acc_holder):
    """Updates both the user and profile tables."""
    try:
        # Update main user table
        db.execute_query("UPDATE users SET name = ? WHERE id = ?", (name, seller_id))
        
        # Update detailed profile
        db.execute_query("""
            UPDATE seller_profiles 
            SET store_name = ?, email = ?, bank_acc = ?, ifsc = ?, branch = ?, acc_holder = ?
            WHERE seller_id = ?
        """, (store_name, email, bank_acc, ifsc, branch, acc_holder, seller_id))
        return True, "Profile Updated Successfully"
    except Exception as e:
        return False, str(e)