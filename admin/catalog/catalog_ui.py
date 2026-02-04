import streamlit as st
import database as db

def render_admin_catalog():
    st.title("🛡️ Global Catalog Management")
    st.caption("Review or remove any product listed on the platform.")

    # Fetch all products + Seller names
    query = """
        SELECT p.product_id, p.name, p.price, p.stock, u.name as seller_name 
        FROM products p 
        JOIN users u ON p.seller_id = u.user_id
    """
    all_prods = db.fetch_query(query)

    if all_prods.empty:
        st.info("No products currently listed.")
    else:
        st.dataframe(all_prods, use_container_width=True, hide_index=True)
        
        # Admin Takedown Feature
        with st.expander("🚨 Product Takedown"):
            target_id = st.number_input("Enter Product ID to Remove", min_value=1, step=1)
            reason = st.text_input("Reason for Takedown")
            if st.button("Delete Product Permanently"):
                db.execute_query("DELETE FROM products WHERE product_id = ?", (target_id,))
                st.warning(f"Product #{target_id} has been removed for: {reason}")
                st.rerun()