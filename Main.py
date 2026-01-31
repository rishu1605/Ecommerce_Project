import streamlit as st
import database 
import cart_logic 
import complaints 
import pandas as pd 

def main():
    st.set_page_config(page_title="SIC Marketplace | Secure Portal", layout="centered")
    
    # Initialize database tables
    database.create_tables()

    # --- SESSION STATE INITIALIZATION ---
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "signup"
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # --- PART A: THE GATEKEEPER (SIGNUP/LOGIN) ---
    if not st.session_state.logged_in:
        if st.session_state.auth_mode == "signup":
            st.header("Create Account")
            is_seller = st.toggle("Register as a Seller")
            role_label = "Seller" if is_seller else "Buyer"
            st.info(f"Registering as a new **{role_label}**")

            with st.form("signup_form"):
                full_name = st.text_input("Full Name" if not is_seller else "Store Name")
                username = st.text_input("Choose Unique Username")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Create Account"):
                    if is_seller:
                        success = database.add_seller(full_name, password)
                    else:
                        success = database.add_user(full_name, username, email, password)
                    
                    if success:
                        st.success("Account created! Please sign in.")
                    else:
                        st.error("Username/Email already exists.")

            if st.button("Already have an account? Sign in"):
                st.session_state.auth_mode = "login"
                st.rerun()
        else:
            st.header("Sign In")
            login_role = st.radio("Account Type:", ["Buyer", "Seller"], horizontal=True)
            user_input = st.text_input("Username" if login_role == "Buyer" else "Store Name")
            pass_input = st.text_input("Password", type="password")

            if st.button("Sign In"):
                if login_role == "Buyer":
                    user = database.login_user(user_input, pass_input)
                else:
                    user = database.login_seller(user_input, pass_input)
                
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_role = login_role
                    st.session_state.user_id = user[0]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

            if st.button("New to SIC? Create an account"):
                st.session_state.auth_mode = "signup"
                st.rerun()

    # --- PART B: THE DASHBOARD (AFTER LOGIN) ---
    else:
        st.sidebar.title(f"👤 {st.session_state.user_role}")
        if st.sidebar.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.cart = []
            st.rerun()

        st.sidebar.divider()

        if st.session_state.user_role == "Buyer":
            menu = ["Shop Products", "My Cart", "File a Complaint"]
        else:
            menu = ["Shop Products", "My Inventory", "Add New Product"]

        choice = st.sidebar.radio("Navigation", menu)

        # --- UPDATED SHOP PRODUCTS SECTION WITH IMAGES ---
        if choice == "Shop Products":
            st.header("🛒 Browse Marketplace")
            
            conn = database.connect_db()
            # Select ALL columns including the new image_url
            df_products = pd.read_sql_query("SELECT * FROM products", conn)
            conn.close()

            if df_products.empty:
                st.info("The marketplace is currently empty.")
            else:
                col_a, col_b = st.columns([2, 1])
                search_q = col_a.text_input("🔍 Search by name...", "")
                categories = ["All"] + sorted(df_products['category'].unique().tolist())
                cat_filter = col_b.selectbox("📁 Category", categories)

                filtered_df = df_products.copy()
                if search_q:
                    filtered_df = filtered_df[filtered_df['name'].str.contains(search_q, case=False)]
                if cat_filter != "All":
                    filtered_df = filtered_df[filtered_df['category'] == cat_filter]

                st.write(f"Showing {len(filtered_df)} products")

                for _, row in filtered_df.iterrows():
                    # Unpack including image_url
                    p_id = row['id']
                    p_name = row['name']
                    p_price = row['price']
                    p_cat = row['category']
                    p_img = row['image_url'] 
                    
                    with st.container():
                        # Layout: Image on the left, details in middle, button on right
                        c1, c2, c3 = st.columns([1.5, 3, 1])
                        
                        if p_img:
                            c1.image(p_img, use_container_width=True)
                        else:
                            c1.info("No Image")
                            
                        c2.write(f"### {p_name}")
                        c2.write(f"**Price:** ${p_price:.2f} | **Category:** {p_cat}")
                        
                        if st.session_state.user_role == "Buyer":
                            if c3.button("Add", key=f"add_{p_id}"):
                                st.session_state.cart.append({"id": p_id, "name": p_name, "price": p_price})
                                st.toast(f"Added {p_name}!")
                        st.divider()

        elif choice == "Add New Product":
            st.header("List New Product")
            with st.form("product_form"):
                name = st.text_input("Product Name")
                price = st.number_input("Price", min_value=0.01)
                # Updated categories to match your product.csv
                cat = st.selectbox("Category", ["Electronic", "Clothing", "Jewelry", "Sports", "Groceries", "Other"])
                img_url = st.text_input("Image URL", placeholder="https://images.unsplash.com/...")
                
                if st.form_submit_button("List Product"):
                    # Call database function with the 5 required arguments
                    database.add_product(name, price, cat, img_url, st.session_state.user_id)
                    st.success(f"✅ {name} listed successfully!")

if __name__ == "__main__":
    main()