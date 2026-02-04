import streamlit as st
import database as db

def render_support_ui():
    st.title("📞 Customer Support")
    user_id = st.session_state.user_data['user_id']
    
    # --- Create Ticket ---
    with st.form("support_form"):
        subject = st.text_input("Subject")
        issue = st.text_area("Describe your issue")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        if st.form_submit_button("Submit Ticket"):
            if subject and issue:
                # First ensure table exists (Dynamic check)
                db.execute_query('''
                    CREATE TABLE IF NOT EXISTS tickets (
                        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        subject TEXT,
                        issue TEXT,
                        status TEXT DEFAULT 'Open',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                db.execute_query(
                    "INSERT INTO tickets (user_id, subject, issue) VALUES (?, ?, ?)",
                    (user_id, subject, issue)
                )
                st.success("Ticket raised! Our team will contact you soon.")
            else:
                st.error("Please fill in all fields.")

    st.markdown("---")
    st.subheader("My Recent Tickets")
    my_tickets = db.fetch_query("SELECT subject, status, created_at FROM tickets WHERE user_id = ?", (user_id,))
    st.table(my_tickets)