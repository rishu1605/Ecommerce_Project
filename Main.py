import streamlit as st
import database as db
from common.theme import apply_custom_theme

# Import entry points for each module
from buyer.buyer_main import run_buyer_ui
from seller.seller_main import run_seller_ui
from admin.admin_main import run_admin_ui

def main():
    st.set_page_config(page_title="SIC Mart | Marketplace", layout="wide", page_icon="🛒")
    apply_custom_theme()

    # Initialize Database Schema
    if 'db_initialized' not in st.session_state:
        db.set_up_tables()
        st.session_state.db_initialized = True

    # Routing via Query Parameters (?page=admin or ?page=seller)
    query_params = st.query_params
    current_page = query_params.get("page", "buyer")

    if current_page == "admin":
        run_admin_ui()
    elif current_page == "seller":
        run_seller_ui()
    else:
        run_buyer_ui()

if __name__ == "__main__":
    main()