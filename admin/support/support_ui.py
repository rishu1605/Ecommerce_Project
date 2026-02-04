import streamlit as st
import database as db

def render_admin_tickets():
    st.title("🎟️ Support Ticket Management")
    
    tickets = db.fetch_query('''
        SELECT t.ticket_id, u.name, u.role, t.subject, t.issue, t.status 
        FROM tickets t 
        JOIN users u ON t.user_id = u.user_id 
        WHERE t.status != 'Resolved'
    ''')
    
    if tickets.empty:
        st.success("All caught up! No open tickets.")
    else:
        for _, row in tickets.iterrows():
            with st.expander(f"Ticket #{row['ticket_id']} - {row['subject']} ({row['role']})"):
                st.write(f"**From:** {row['name']}")
                st.write(f"**Issue:** {row['issue']}")
                if st.button("Mark as Resolved", key=f"res_{row['ticket_id']}"):
                    db.execute_query("UPDATE tickets SET status='Resolved' WHERE ticket_id=?", (row['ticket_id'],))
                    st.rerun()