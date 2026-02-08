import streamlit as st
from common.theme import apply_custom_theme

# NOTE: We do NOT import sub-modules (buyer_main, etc.) at the top level 
# if they import 'database' or 'Main', to avoid Circular Import KeyErrors.

def main():
    # 1. PAGE CONFIG (Must be the very first Streamlit command)
    st.set_page_config(
        page_title="SIC Mart | Smart • Instant • Choice", 
        layout="wide", 
        page_icon="🛒"
    )
    
    # 2. LOCAL IMPORTS (The "Careful" Part)
    # Importing database inside main() prevents the 'KeyError' during initialization
    import database as db
    from buyer.buyer_main import run_buyer_ui
    from seller.seller_main import run_seller_ui
    from admin.admin_main import run_admin_ui

    # 3. APPLY THEME
    apply_custom_theme()

    # 4. INITIALIZE DATABASE
    # We use a try-except block to catch connection issues immediately
    try:
        if 'db_initialized' not in st.session_state:
            db.set_up_tables()
            st.session_state.db_initialized = True
    except Exception as e:
        st.error(f"Critical Error: Could not connect to database. {e}")
        return

    # 5. ROUTING LOGIC
    # Using the new st.query_params API
    query_params = st.query_params
    current_page = query_params.get("page", "buyer")

    # 6. PORTAL ROUTING
    if current_page == "admin":
        run_admin_ui()
    elif current_page == "seller":
        run_seller_ui()
    else:
        # Defaults to Buyer UI
        run_buyer_ui()

if __name__ == "__main__":
    main()