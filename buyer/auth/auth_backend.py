import database as db

def authenticate_user(email, password):
    query = "SELECT * FROM users WHERE email = ? AND password = ?"
    result = db.fetch_query(query, (email, password))
    return result.iloc[0].to_dict() if not result.empty else None

def register_user(name, email, password, role="buyer"):
    check_query = "SELECT * FROM users WHERE email = ?"
    existing = db.fetch_query(check_query, (email,))
    if not existing.empty:
        return False, "Email already registered!"
    
    try:
        insert_query = "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)"
        db.execute_query(insert_query, (name, email, password, role))
        return True, "Registration Successful!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verify_email_exists(email):
    query = "SELECT * FROM users WHERE email = ?"
    result = db.fetch_query(query, (email,))
    return not result.empty

def reset_password(email, new_password):
    try:
        query = "UPDATE users SET password = ? WHERE email = ?"
        db.execute_query(query, (new_password, email))
        return True
    except:
        return False