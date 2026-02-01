import streamlit as st
import database
import os
import json

def main():
    st.set_page_config(page_title="SIC Marketplace", layout="wide")
    database.create_tables()

    # Initialize session states
    if 'user' not in st.session_state: st.session_state.user = None
    if 'cart' not in st.session_state: st.session_state.cart = {}

    if not st.session_state.user:
        render_login()
    else:
        render_dashboard()

def render_login():
    st.title("🛍️ SIC Amazon-Style Marketplace")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Username")
        role = st.selectbox("Role", ["Buyer", "Seller", "Admin"])
    if st.button("Login / Register"):
        # For deployment/study, we simulate a user ID
        st.session_state.user = {"name": name, "role": role, "id": 1} 
        st.rerun()

def render_dashboard():
    user = st.session_state.user
    st.sidebar.header(f"👤 Account: {user['name']}")
    
    # NAVIGATION LOGIC
    if user['role'] == "Buyer":
        menu = st.sidebar.radio("Navigation", ["Marketplace", "My Cart", "Customer Support"])
        
        if menu == "Marketplace":
            render_marketplace()
        elif menu == "My Cart":
            render_cart()
        elif menu == "Customer Support":
            render_complaints()
            
    elif user['role'] == "Seller":
        render_seller_dashboard()
        
    elif user['role'] == "Admin":
        render_admin_dashboard()

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.cart = {}
        st.rerun()

# --- BUYER FEATURES ---

def render_marketplace():
    st.title("🛍️ SIC Global Marketplace")
    
    # 1. Category Filter
    category = st.selectbox("Filter by Category", ["All", "Electronics", "Grocery", "Clothing", "Sports", "Jewelry", "Health"])
    
    conn = database.connect_db()
    cursor = conn.cursor()
    if category == "All":
        cursor.execute("SELECT * FROM products")
    else:
        cursor.execute("SELECT * FROM products WHERE category=?", (category,))
    products = cursor.fetchall()
    conn.close()

    if not products:
        st.warning("No products found in this category.")
    else:
        cols = st.columns(3)
        for i, p in enumerate(products):
            with cols[i % 3]:
                # IMAGE HANDLER: Uses placeholder if local file is missing
                imgs = p[7].split("|")
                if os.path.exists(imgs[0]):
                    st.image(imgs[0], use_container_width=True)
                else:
                    # Professional placeholder for missing study images
                    st.image("https://via.placeholder.com/250?text=SIC+Product", caption="Demo Image")
                
                st.subheader(p[1])
                st.write(f"**Price:** ${p[2]}")
                
                # DETAILED VIEW FEATURE
                with st.expander("🔍 View Details & Specs"):
                    st.write(f"**Stock Available:** {p[5]} units")
                    st.write("**Specifications:**")
                    specs = p[6].split('*')
                    for s in specs:
                        if s.strip(): st.write(f"• {s.strip()}")
                    
                    # Show alternative angles if they exist
                    if len(imgs) > 1:
                        st.write("**More Angles:**")
                        sub_cols = st.columns(len(imgs)-1)
                        for idx, extra_img in enumerate(imgs[1:]):
                            if os.path.exists(extra_img):
                                sub_cols[idx].image(extra_img, width=80)

                if st.button(f"🛒 Add to Cart", key=f"add_{p[0]}"):
                    st.session_state.cart[p[0]] = {"name": p[1], "price": p[2], "qty": 1}
                    st.toast(f"Added {p[1]} to cart!")

def render_cart():
    st.title("🛒 Your Shopping Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty. Go to the Marketplace to add items.")
    else:
        total = 0
        for pid, item in list(st.session_state.cart.items()):
            col1, col2, col3 = st.columns([4, 1, 1])
            col1.write(f"**{item['name']}**")
            col2.write(f"${item['price']}")
            if col3.button("Remove", key=f"rem_{pid}"):
                del st.session_state.cart[pid]
                st.rerun()
            total += item['price']
        
        st.divider()
        st.subheader(f"Total Amount: ${total}")
        
        # PAYMENT SECTION
        st.write("### 💳 Payment Gateway")
        method = st.radio("Select Payment Method", ["UPI", "Credit/Debit Card", "Net Banking"])
        if st.button("Complete Transaction"):
            success, msg = database.process_payment(st.session_state.user['id'], st.session_state.cart, total, method)
            if success:
                st.success(f"Payment Successful via {method}! Order ID: {msg}")
                st.balloons()
                st.session_state.cart = {} # Clear cart
            else:
                st.error(f"Transaction Failed: {msg}")

def render_complaints():
    st.title("📝 Customer Support & Complaints")
    st.write("Having an issue with your order? Let us know.")
    
    with st.form("complaint_form"):
        subject = st.text_input("Subject")
        issue_type = st.selectbox("Issue Type", ["Late Delivery", "Damaged Product", "Payment Issue", "Other"])
        description = st.text_area("Detailed Description")
        
        if st.form_submit_button("Submit Complaint"):
            # Logic to save to complaints_db.json
            complaint_data = {
                "user": st.session_state.user['name'],
                "subject": subject,
                "type": issue_type,
                "desc": description
            }
            # Append logic (simple file storage for project)
            with open("complaints_db.json", "a") as f:
                f.write(json.dumps(complaint_data) + "\n")
            st.success("Complaint submitted successfully. Our team will review it.")

# --- SELLER & ADMIN FEATURES ---

def render_seller_dashboard():
    st.header("📤 Seller Portal")
    with st.form("list_item"):
        name = st.text_input("Product Name")
        price = st.number_input("Price ($)", min_value=0.1)
        cat = st.selectbox("Category", ["Electronics", "Grocery", "Clothing", "Sports", "Jewelry", "Health"])
        stock = st.number_input("Stock", min_value=1)
        specs = st.text_area("Specifications (e.g. *Waterproof *1 Year Warranty)")
        files = st.file_uploader("Upload 3-10 Product Images", accept_multiple_files=True, type=['jpg','png'])
        
        if st.form_submit_button("List Product"):
            if 3 <= len(files) <= 10:
                img_paths = database.save_images_locally(files, name)
                # Ensure your database.py has an add_product function
                # database.add_product(name, price, cat, stock, specs, img_paths)
                st.success(f"Product '{name}' is now live!")
            else:
                st.error("Error: You must upload between 3 and 10 images.")

def render_admin_dashboard():
    st.header("📊 Administrator Dashboard")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Products CSV"):
            file = database.export_csv("products")
            st.success(f"Exported to {file}")
            
    with col2:
        if st.button("Export Orders CSV"):
            file = database.export_csv("orders")
            st.success(f"Exported to {file}")

    st.write("### Review Complaints")
    if os.path.exists("complaints_db.json"):
        with open("complaints_db.json", "r") as f:
            for line in f:
                c = json.loads(line)
                st.info(f"**From:** {c['user']} | **Subject:** {c['subject']}\n\n{c['desc']}")
    else:
        st.write("No complaints filed yet.")

if __name__ == "__main__":
    main()