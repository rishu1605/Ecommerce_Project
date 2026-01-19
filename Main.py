import streamlit as st
import storage
import complaints
import cart_logic

def main():
    st.set_page_config(page_title="SIC E-Commerce", layout="wide")
    
    # 1. Initialize Session State (This keeps the cart active)
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to:", ["Home", "My Cart", "File a Complaint", "Admin"])

    # --- OPTION 1: PRODUCTS ---
    if choice == "Home":

        search_query=st.text_input("Search Products",placeholder="Search By Product Name")
        # st.header("Available Products")
        

        col1, col2 = st.columns([1, 3])
        with col1:
         selected_category = st.selectbox("Category",["All", "Electronics", "Men Wearing", "Women Wearing"],
        label_visibility="collapsed" # Hides the label to keep it compact
        )

        # products = [
        #     {"id": 101, "name": "Laptop", "price": 800,"category": "Electronics"},
        #     {"id": 102, "name": "Headphones", "price": 50,"category": "Electronics"},
        #     {"id":103,"name":"Mouse","price":20,"category": "Electronics"},
        #     {"id":104,"name":"Phone","price":399,"category": "Electronics"},
        #     {"id":105,"name":"Type-C Charger","price":15,"category": "Electronics"},
        #     {"id":106,"name":"SmartWatch","price":169,"category": "Electronics"},
        #     {"id": 201, "name": "Men T-Shirt", "price": 20, "category": "Men Wearing"},
        #     {"id": 202, "name": "Men Jeans", "price": 40, "category": "Men Wearing"},
        #     {"id": 301, "name": "Women Dress", "price": 45, "category": "Women Wearing"},
        #     {"id": 302, "name": "Women Saree", "price": 70, "category": "Women Wearing"},
        # ]
        from PIL import Image
        products = [
    {
        "id": 201,
        "name": "Men Leather Jacket",
        "price": 20,
        "category": "Men Wearing",
        "desc": "Stylish Men Jacket best for winter Wearing",
        "img": "images/leatherjacket.png"
    },
]

     

       

        
        found=False
        for p in products:
            category_selection=(selected_category =="All" or p["category"] == selected_category)

            search_match = search_query.lower() in p["name"].lower()
            
            if category_selection and search_match:
                found=True
                # col1, col2 = st.columns([3,1])
                # col1.write(f"*{p['name']}* - ${p['price']}")

                # if col2.button(f"Add to Cart", key=p['id']):
                #     st.session_state.cart.append(p)
                #     st.balloons()
                #     st.toast("🎉 Item Added successfully")

                col_img, col_info, col_btn,col_btn_2 = st.columns([1, 3, 1, 1])

        # 📷 Image (Left)
        with col_img:
            st.image(p["img"],width=1800)
            img = Image.open(p["img"])

        # ℹ️ Name + Description (Center)
        with col_info:
            st.subheader(p["name"])
            st.caption(p["desc"])
            st.write(f"Price: ${p['price']}")

        # 🛒 Button (Right)
        with col_btn:
            st.write("")  # spacing
            st.write("")
            if st.button("Add to Cart", key=p["id"]):
                st.session_state.cart.append(p)
                st.balloons()
                st.toast("🎉 Item added successfully")

        with col_btn_2:
            st.write("")  # spacing
            st.write("")
            if st.button("Buy Now", key=f"buy_{p['id']}"):
                st.session_state.cart.append(p)
                st.toast("Directing to Buying Page")

        st.divider()

        if not found:
                    st.info("No products found for your search")
        

    # --- OPTION 4: COMPLAINTS ---
    elif choice == "File a Complaint":
        st.header("Help & Support")
        with st.form("complaint_form"):
            u_name = st.text_input("Name")
            msg = st.text_area("What is your issue?")
            pri = st.select_slider("Priority", options=["Low", "Medium", "High"])
            submit = st.form_submit_button("Submit Ticket")
            
            if submit:
                # Structured data logic
                new_ticket = {"user": u_name, "issue": msg, "priority": pri, "status": "Open"}
                existing_data = storage.load_data("complaints_db.json")
                existing_data.append(new_ticket)
                storage.save_data("complaints_db.json", existing_data)
                st.success("Complaint Filed Successfully!")

if __name__ == "__main__":
    main()