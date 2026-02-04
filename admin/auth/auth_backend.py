import database as db
from common.auth_utils import verify_password

def login_admin(uid, password):
    """
    Authenticates the administrator. 
    Registration is disabled for security; accounts must be pre-seeded.
    """
    # Specifically check for the 'admin' role to prevent role-escalation attacks
    query = "SELECT * FROM users WHERE id = ? AND role = 'admin'"
    user_df = db.fetch_query(query, (uid,))
    
    if user_df.empty:
        return None, "Access Denied: Not an Admin account."
    
    stored_hash = user_df.iloc[0]['password']
    
    if verify_password(password, stored_hash):
        return user_df.iloc[0].to_dict(), "System Access Granted."
    
    return None, "Invalid Security Credentials."