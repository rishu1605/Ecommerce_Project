import database as db

def get_admin_profile(admin_id):
    """Fetches administrative user details."""
    return db.fetch_query("""
        SELECT id, name, role FROM users 
        WHERE id = ? AND role = 'admin'
    """, (admin_id,))

def update_admin_profile(admin_id, new_name):
    """Updates the administrator's display name."""
    try:
        db.execute_query("UPDATE users SET name = ? WHERE id = ?", (new_name, admin_id))
        return True, "Administrator Profile Updated"
    except Exception as e:
        return False, str(e)