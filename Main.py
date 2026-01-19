import streamlit as st
import storage
import cart_logic

# --- PAGE SETUP ---
st.set_page_config(page_title="SIC Premium Marketplace", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'complaints' not in st.session_state: st.session_state.complaints = []
if 'view_item' not in st.session_state: st.session_state.view_item = None

inventory = storage.load_products()

# --- BIG SCREEN DETAIL VIEW ---
if st.session_state.view_item:
    p = st.session_state.view_item
    
    # 1. THE STEADY FIX: Move the Back button to the Sidebar 
    # This keeps it visible NO MATTER how far down you scroll on the main page.
    st.sidebar.divider()
    st.sidebar.subheader("🎯 Navigation")
    if st.sidebar.button("⬅️ Back to Marketplace", use_container_width=True, type="primary"):
        st.session_state.view_item = None
        st.rerun()
    
    st.sidebar.info("The marketplace is hidden while you view these specifications.")

    # 2. Main Content
    st.title(p["name"])
    st.write(f"### Price: ${p['price']} | {p['rating']}")
    
    col_img, col_info = st.columns([1, 1])
    
    with col_img:
        st.image(p["image"], use_column_width=True)
        # Add a redundant button here just in case
        if st.button("Add to Shopping Cart", type="primary", use_container_width=True):
            cart_logic.add_to_cart(p)
    
    with col_info:
        st.write("### 🛠️ Technical Specifications")
        spec_data = {
            "Manufacturer": p["mfr"],
            "Model Number": p["model"],
            "Year": p["year"],
            "Dimensions": p["dimensions"],
            "Weight": p["weight"],
            "Material": p["material"]
        }
        st.table(spec_data)
        
    st.divider()
    
    # Long content that causes scrolling
    st.subheader("📝 Detailed Features")
    st.write(p["specs"])
    
    st.subheader("🧼 Care & Maintenance")
    st.write(p["care"])
    
    # Adding extra space to test the "Steady" button in the sidebar
    st.write(" " * 100) 
            
    st.stop()

# --- MAIN NAVIGATION ---
st.sidebar.title("🏢 SIC Navigation")
choice = st.sidebar.radio("Go to:", ["Marketplace", "My Cart", "File a Complaint", "Admin Panel"])

# --- MARKETPLACE ---
if choice == "Marketplace":
    st.title("🌐 SIC Global Marketplace")
    
    c1, c2 = st.columns([3, 1])
    with c1: search = st.text_input("🔍 Search Inventory...")
    with c2: cat = st.selectbox("Category", ["All", "Gadgets", "Machinery", "Sports", "Clothing"])

    filtered = [p for p in inventory if (cat == "All" or p['category'] == cat) and (search.lower() in p['name'].lower())]

    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(filtered):
                item = filtered[i+j]
                with cols[j]:
                    with st.container(border=True):
                        st.image(item["image"], use_column_width=True)
                        st.subheader(item["name"])
                        st.write(f"**Price:** ${item['price']} | **Model:** {item['model']}")
                        if st.button("View Full Specifications", key=f"view_{item['id']}", use_container_width=True):
                            st.session_state.view_item = item
                            st.rerun()

# --- ADVANCED MY CART ---
elif choice == "My Cart":
    st.title("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        # Check if they JUST placed an order (to show success instead of "empty")
        if st.session_state.get('order_success'):
            st.balloons()
            st.success("🎉 **Order Placed Successfully!**")
            st.write("Thank you for shopping with SIC Marketplace. Your order ID is #SIC-778210.")
            st.info("A confirmation invoice has been sent to your email.")
            if st.button("Continue Shopping"):
                st.session_state.order_success = False
                st.rerun()
        else:
            st.info("Your cart is empty.")
    else:
        col_list, col_summary = st.columns([2, 1])
        
        with col_list:
            for idx, item in enumerate(st.session_state.cart):
                with st.container(border=True):
                    ca, cb, cc = st.columns([1, 2, 1])
                    with ca: 
                        st.image(item["image"], width=100)
                    with cb:
                        st.subheader(item["name"])
                        st.write(f"**Model:** {item['model']} ({item['year']})")
                    with cc:
                        st.write(f"### ${item['price']}")
                        if st.button("🗑️ Remove", key=f"rem_{idx}", use_container_width=True):
                            cart_logic.remove_from_cart(idx)
        
        with col_summary:
            with st.container(border=True):
                st.header("Summary")
                total = cart_logic.calculate_total()
                st.write(f"Total Items: {len(st.session_state.cart)}")
                st.divider()
                st.title(f"Total: ${total}")
                
                if st.button("🚀 Proceed to Checkout", type="primary", use_container_width=True):
                    # Set a flag to show success message after rerun
                    st.session_state.order_success = True
                    st.session_state.cart = [] # Clear the cart
                    st.rerun()

# --- OTHER PAGES ---
elif choice == "File a Complaint":
    st.title("📩 Customer Support")
    st.write("Encountered an issue with a product? Let us know.")
    
    with st.form("complaint_form", clear_on_submit=True):
        u_name = st.text_input("Full Name")
        u_prod = st.selectbox("Select Product", [p['name'] for p in inventory])
        u_msg = st.text_area("Issue Details (e.g., technical fault, delivery delay)")
        
        if st.form_submit_button("Submit Complaint"):
            if u_name and u_msg:
                cart_logic.save_complaint(u_name, u_prod, u_msg)
                st.success("Complaint submitted successfully to the Admin Panel.")
            else:
                st.error("Please fill in all fields.")

elif choice == "Admin Panel":
    st.title("📊 Admin Dashboard")
    st.subheader("Recent Customer Complaints")
    
    if st.session_state.complaints:
        # Displaying as a professional table
        st.table(st.session_state.complaints)
        if st.button("Clear All Complaints"):
            st.session_state.complaints = []
            st.rerun()
    else:
        st.info("No pending complaints in the system, THANKYOU!")