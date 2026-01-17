import interface
import storage
import complaints

def main():
    # 1. Initialize data
    products = [
        {"id": 101, "name": "Laptop", "price": 800},
        {"id": 102, "name": "Headphones", "price": 50}
    ]
    all_complaints = storage.load_data("complaints_db.json")

    # 2. THE LOOP (This keeps the terminal from closing)
    running = True
    while running:
        interface.show_menu()
        choice = input("Select an option (1-6): ")

        if choice == '1':
            interface.product_list(products)
        elif choice == '6':
            print("Exiting system...")
            running = False # This breaks the loop
        else:
            print(f"You chose {choice}. This feature is under development!")

# 3. THE TRIGGER (This starts the function)
if __name__ == "__main__":
    main()