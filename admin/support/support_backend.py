import database as db

def get_all_tickets():
    return db.fetch_query("""
        SELECT t.ticket_id, u.name, u.role, t.subject, t.issue, t.status 
        FROM tickets t 
        JOIN users u ON t.user_id = u.user_id 
        WHERE t.status != 'Resolved'
    """)

def resolve_ticket(ticket_id):
    db.execute_query("UPDATE tickets SET status = 'Resolved' WHERE ticket_id = ?", (ticket_id,))