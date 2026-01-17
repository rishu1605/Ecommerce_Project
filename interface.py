def show_menu():
    print("\n--- 🛒 E-COMMERCE CART SYSTEM ---")
    print("1. View Available Products")
    print("2. Add Item to Cart")
    print("3. View Cart & Checkout")
    print("4. 📩 File a Complaint")
    print("5. 🛠 Admin: View Complaints")
    print("6. Exit")

def product_list(products):
    print("\nID | Name | Price")
    for p in products:
        print(f"{p['id']} | {p['name']} | ${p['price']}")