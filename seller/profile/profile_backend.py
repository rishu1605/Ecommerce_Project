import database as db

def get_full_seller_profile(seller_id):
    """Fetches combined data from users and seller_profiles tables."""
    # Data Mapping: 
    # users (u) stores: name, email, bank_acc, ifsc, branch, acc_holder
    # seller_profiles (s) stores: store_name, pan_number
    return db.fetch_query("""
        SELECT u.name, u.user_id, s.store_name, u.email, s.pan_number as pan, 
               u.bank_acc, u.ifsc, u.branch, u.acc_holder
        FROM users u
        JOIN seller_profiles s ON u.user_id = s.seller_id
        WHERE u.user_id = ?
    """, (seller_id,))

def update_seller_profile(seller_id, name, store_name, email, bank_acc, ifsc, branch, acc_holder):
    """Updates both the user and profile tables according to the schema."""
    try:
        # 1. Update personal & banking info in 'users' table
        db.execute_query("""
            UPDATE users 
            SET name = ?, email = ?, bank_acc = ?, ifsc = ?, branch = ?, acc_holder = ? 
            WHERE user_id = ?
        """, (name, email, bank_acc, ifsc, branch, acc_holder, seller_id))
        
        # 2. Update business-specific info in 'seller_profiles' table
        db.execute_query("""
            UPDATE seller_profiles 
            SET store_name = ?
            WHERE seller_id = ?
        """, (store_name, seller_id))
        
        return True, "Profile Updated Successfully"
    except Exception as e:
        return False, str(e)