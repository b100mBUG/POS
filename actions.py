from database import session
from database import Product, User, Transaction, Cylinder

def add_user():
    user_name = input("Enter Username: ")
    user_password = input("Enter User Password: ")
    user_role = input("Enter User Role: ")

    session.add(User(user_name = user_name, user_password = user_password, user_role = user_role))
    session.commit()
    print("User added successfully...")

def add_item():
    item_name = input("Enter item name: ")
    item_categroy = input("Enter item category: ")
    item_desc = input("Enter item description: ")
    item_quantity = input("Enter item quantity: ")
    item_price = input("Enter item price: ")
    item_image = input("Enter item image: ")
    new_item = Product(
        prod_name = item_name, 
        prod_category = item_categroy, 
        prod_desc = item_desc, 
        product_image = item_image,
        prod_price = item_price,
        quantity = item_quantity
    )

    session.add(new_item)
    session.commit()
    print("Item added successfully...")

def show_users():
    users = session.query(User).all()
    for user in users:
        print(f"\nName: {user.user_name}\nRole: {user.user_role}\nPassword: {user.user_password}\nDate Added: {user.date_added}\nExpiry date: {user.expiry_date}")

def show_gases():
    gases = session.query(Cylinder).all()
    for gas in gases:
        print(f"\nName: {gas.cylinder_name}\nLocation: {gas.cylinder_loc}\n6Kg: {gas.six_kg_count}\n13Kg: {gas.thirteen_kg_count}\n3Kg: {gas.three_kg_count}\n50Kg: {gas.fifty_kg_count}")


def show_items():
    items = session.query(Product).all()
    for item in items:
        print(f"\nName: {item.prod_name}\nCategory: {item.prod_category}\nDescription: {item.prod_desc}\nDate Added: {item.date_added}\nImage: {item.product_image}\nQuantity: {item.quantity}\nPrice: {item.prod_price}")

def delete_prod():
    session.query(Product).delete()
    session.commit()
    print("Products deleted successfully...")

def delete_cylinders():
    session.query(Cylinder).delete()
    session.commit()
    print("Cylinders deleted successfully...")

def delete_transanctions():
    session.query(Transaction).delete()
    session.commit()
    print("Transactions deleted successfully...")

def delete_users():
    session.query(User).delete()
    session.commit()
    print("Users deleted successfully...")

def main():
    actions = [
        "Add Items",
        "Add Users",
        "Show Items",
        "Show Users",
        "Show Cylinders",
        "Delete Products",
        "Delete Transactions",
        "Delete Cylinders",
        "Delete Users"
    ]
    count = 1
    print("\n")
    for action in actions:
        print(f"{count}. {action}")
        count += 1
    while True:
        print("\n")
        choice = int(input("Enter Choice: "))
        print("\n")
        if choice == 1:
            add_item()
        elif choice == 2:
            add_user()
        elif choice == 3:
            show_items()
        elif choice == 4:
            show_users()
        elif choice == 5:
            show_gases()
        elif choice == 6:
            delete_prod()
        elif choice == 7:
            delete_transanctions()
        elif choice == 8:
            delete_cylinders()
        elif choice == 9:
            delete_users()

if __name__ == "__main__":
    main()
