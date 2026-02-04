import database as db

def get_all_users_count():
    return db.fetch_query("SELECT role, COUNT(*) as count FROM users GROUP BY role")

def get_detailed_user_list():
    return db.fetch_query("SELECT user_id, name, email, role FROM users")

def update_user_role(user_id, new_role):
    db.execute_query("UPDATE users SET role = ? WHERE user_id = ?", (new_role, user_id))

def delete_user(user_id):
    # Note: In a real app, you might want to 'deactivate' rather than delete
    db.execute_query("DELETE FROM users WHERE user_id = ?", (user_id,))
    db.execute_query("DELETE FROM wallets WHERE user_id = ?", (user_id,))