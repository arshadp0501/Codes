import json
import os

class Item:
    def __init__(self, name, category, quantity, price):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
        return f"Item: {self.name}, Category: {self.category}, Quantity: {self.quantity}, Price: ${self.price}"

    def update_quantity(self, quantity):
        if quantity >= 0:
            self.quantity = quantity
        else:
            print("Quantity cannot be negative.")
    
    def update_price(self, price):
        if price >= 0:
            self.price = price
        else:
            print("Price cannot be negative.")
    
    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price
        }

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role
    
    def __str__(self):
        return f"User: {self.username}, Role: {self.role}"

class Inventory:
    def __init__(self):
        self.items = {}
        self.users = {}
        self.load_inventory()

    def add_item(self, name, category, quantity, price):
        if name in self.items:
            print(f"Item {name} already exists. Use update functionality instead.")
        else:
            new_item = Item(name, category, quantity, price)
            self.items[name] = new_item
            print(f"Item {name} added successfully.")

    def update_item(self, name, quantity=None, price=None):
        if name not in self.items:
            print(f"Item {name} does not exist.")
        else:
            item = self.items[name]
            if quantity is not None:
                item.update_quantity(quantity)
            if price is not None:
                item.update_price(price)
            print(f"Item {name} updated successfully.")
    
    def delete_item(self, name):
        if name in self.items:
            del self.items[name]
            print(f"Item {name} deleted successfully.")
        else:
            print(f"Item {name} not found.")
    
    def view_item(self, name):
        if name in self.items:
            print(self.items[name])
        else:
            print(f"Item {name} not found.")
    
    def list_items(self):
        if not self.items:
            print("No items in inventory.")
        else:
            for item in self.items.values():
                print(item)
    
    def add_user(self, username, role):
        if username in self.users:
            print(f"User {username} already exists.")
        else:
            new_user = User(username, role)
            self.users[username] = new_user
            print(f"User {username} added successfully.")
    
    def view_user(self, username):
        if username in self.users:
            print(self.users[username])
        else:
            print(f"User {username} not found.")
    
    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            print(f"User {username} deleted successfully.")
        else:
            print(f"User {username} not found.")
    
    def load_inventory(self):
        if os.path.exists('inventory.json'):
            with open('inventory.json', 'r') as file:
                data = json.load(file)
                self.items = {item['name']: Item(**item) for item in data['items']}
                self.users = {user['username']: User(**user) for user in data['users']}
                print("Inventory loaded successfully.")
        else:
            print("No existing inventory found. Starting fresh.")
    
    def save_inventory(self):
        data = {
            'items': [item.to_dict() for item in self.items.values()],
            'users': [user.__dict__ for user in self.users.values()]
        }
        with open('inventory.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully.")
    
    def login(self, username):
        if username in self.users:
            print(f"Welcome, {username}!")
        else:
            print(f"User {username} not found.")
    
    def logout(self):
        print("Logged out successfully.")

class InventorySystem:
    def __init__(self):
        self.inventory = Inventory()
        self.logged_in_user = None

    def main_menu(self):
        while True:
            if self.logged_in_user:
                print(f"\nWelcome {self.logged_in_user.username} ({self.logged_in_user.role})")
            else:
                print("\nWelcome to the Inventory System")
            print("\nMain Menu:")
            print("1. View All Items")
            print("2. Add Item")
            print("3. Update Item")
            print("4. Delete Item")
            print("5. View Item")
            print("6. Manage Users")
            print("7. Save Inventory")
            print("8. Logout")
            print("9. Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                self.view_items()
            elif choice == '2':
                self.add_item()
            elif choice == '3':
                self.update_item()
            elif choice == '4':
                self.delete_item()
            elif choice == '5':
                self.view_single_item()
            elif choice == '6':
                self.manage_users()
            elif choice == '7':
                self.inventory.save_inventory()
            elif choice == '8':
                self.logout()
            elif choice == '9':
                self.exit_system()
            else:
                print("Invalid choice. Please try again.")
    
    def view_items(self):
        self.inventory.list_items()
    
    def add_item(self):
        name = input("Enter item name: ")
        category = input("Enter item category: ")
        quantity = int(input("Enter item quantity: "))
        price = float(input("Enter item price: "))
        self.inventory.add_item(name, category, quantity, price)
    
    def update_item(self):
        name = input("Enter item name to update: ")
        quantity = input("Enter new quantity (leave blank for no change): ")
        price = input("Enter new price (leave blank for no change): ")
        quantity = int(quantity) if quantity else None
        price = float(price) if price else None
        self.inventory.update_item(name, quantity, price)
    
    def delete_item(self):
        name = input("Enter item name to delete: ")
        self.inventory.delete_item(name)
    
    def view_single_item(self):
        name = input("Enter item name to view: ")
        self.inventory.view_item(name)
    
    def manage_users(self):
        print("\nManage Users:")
        print("1. Add User")
        print("2. View User")
        print("3. Delete User")
        print("4. Back to Main Menu")
        
        choice = input("Choose an option: ")
        if choice == '1':
            self.add_user()
        elif choice == '2':
            self.view_user()
        elif choice == '3':
            self.delete_user()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")
    
    def add_user(self):
        username = input("Enter username: ")
        role = input("Enter role (Admin/User): ")
        self.inventory.add_user(username, role)
    
    def view_user(self):
        username = input("Enter username to view: ")
        self.inventory.view_user(username)
    
    def delete_user(self):
        username = input("Enter username to delete: ")
        self.inventory.delete_user(username)
    
    def logout(self):
        print("Logging out...")
        self.logged_in_user = None
        self.main_menu()
    
    def exit_system(self):
        print("Saving data and exiting the system...")
        self.inventory.save_inventory()
        print("Goodbye!")
        exit()

def main():
    system = InventorySystem()
    system.main_menu()

if __name__ == '__main__':
    main()
