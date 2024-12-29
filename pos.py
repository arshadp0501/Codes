import json
import os
from datetime import datetime

class Item:
    def __init__(self, item_id, name, price, quantity):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def update_quantity(self, quantity):
        if quantity >= 0:
            self.quantity = quantity
        else:
            print("Quantity cannot be negative.")
    
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }
    
    def __str__(self):
        return f"Item ID: {self.item_id}, Name: {self.name}, Price: ${self.price}, Quantity: {self.quantity}"

class Customer:
    def __init__(self, customer_id, name, email, phone):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
    
    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}"

class Transaction:
    def __init__(self, transaction_id, customer, items):
        self.transaction_id = transaction_id
        self.customer = customer
        self.items = items
        self.date = datetime.now()
        self.total_amount = self.calculate_total()
        self.tax = self.calculate_tax()
        self.final_amount = self.total_amount + self.tax
    
    def calculate_total(self):
        return sum(item.price * item.quantity for item in self.items)
    
    def calculate_tax(self):
        return self.total_amount * 0.1  # Assume 10% sales tax
    
    def generate_receipt(self):
        receipt = f"Receipt for Transaction ID: {self.transaction_id}\n"
        receipt += f"Customer: {self.customer.name} | {self.customer.email}\n"
        receipt += f"Date: {self.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "-" * 40 + "\n"
        for item in self.items:
            receipt += f"{item.name} (x{item.quantity}) - ${item.price * item.quantity}\n"
        receipt += "-" * 40 + "\n"
        receipt += f"Subtotal: ${self.total_amount}\n"
        receipt += f"Tax (10%): ${self.tax}\n"
        receipt += f"Total: ${self.final_amount}\n"
        receipt += "-" * 40 + "\n"
        return receipt

class POS:
    def __init__(self):
        self.inventory = {}
        self.customers = {}
        self.transactions = {}
        self.load_inventory()

    def load_inventory(self):
        """Load items and customers from JSON files."""
        if os.path.exists("inventory.json"):
            with open("inventory.json", "r") as file:
                data = json.load(file)
                self.inventory = {item["item_id"]: Item(**item) for item in data["items"]}
                print("Inventory loaded.")
        if os.path.exists("customers.json"):
            with open("customers.json", "r") as file:
                data = json.load(file)
                self.customers = {customer["customer_id"]: Customer(**customer) for customer in data["customers"]}
                print("Customer data loaded.")

    def save_inventory(self):
        """Save the current state of inventory and customers to JSON files."""
        data = {
            "items": [item.to_dict() for item in self.inventory.values()],
            "customers": [customer.__dict__ for customer in self.customers.values()]
        }
        with open("inventory.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved.")

    def add_item(self, item_id, name, price, quantity):
        if item_id in self.inventory:
            print(f"Item {name} already exists.")
        else:
            self.inventory[item_id] = Item(item_id, name, price, quantity)
            print(f"Item {name} added successfully.")
    
    def update_item_quantity(self, item_id, quantity):
        if item_id in self.inventory:
            self.inventory[item_id].update_quantity(quantity)
            print(f"Quantity for item ID {item_id} updated to {quantity}.")
        else:
            print(f"Item ID {item_id} not found.")
    
    def list_items(self):
        """List all available items in inventory."""
        if not self.inventory:
            print("No items available.")
        else:
            for item in self.inventory.values():
                print(item)
    
    def add_customer(self, customer_id, name, email, phone):
        if customer_id in self.customers:
            print(f"Customer with ID {customer_id} already exists.")
        else:
            self.customers[customer_id] = Customer(customer_id, name, email, phone)
            print(f"Customer {name} added successfully.")
    
    def process_sale(self, customer_id, items_in_cart):
        if customer_id not in self.customers:
            print(f"Customer with ID {customer_id} not found.")
            return
        
        customer = self.customers[customer_id]
        transaction_id = len(self.transactions) + 1
        items = []
        
        for item_id, quantity in items_in_cart.items():
            if item_id in self.inventory and self.inventory[item_id].quantity >= quantity:
                item = self.inventory[item_id]
                item.update_quantity(item.quantity - quantity)
                items.append(Item(item_id, item.name, item.price, quantity))
            else:
                print(f"Item ID {item_id} is not available or quantity is insufficient.")
        
        if items:
            transaction = Transaction(transaction_id, customer, items)
            self.transactions[transaction_id] = transaction
            print(f"Transaction {transaction_id} completed.")
            print(transaction.generate_receipt())
        else:
            print("No valid items in the cart. Transaction failed.")

    def generate_sales_report(self):
        """Generate a report of all transactions."""
        if not self.transactions:
            print("No transactions found.")
            return
        
        report = "Sales Report\n"
        report += "-" * 40 + "\n"
        for transaction in self.transactions.values():
            report += f"Transaction ID: {transaction.transaction_id}\n"
            report += f"Customer: {transaction.customer.name}\n"
            report += f"Date: {transaction.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += f"Total: ${transaction.final_amount}\n"
            report += "-" * 40 + "\n"
        return report
    
    def exit_system(self):
        """Exit the system and save the data."""
        print("Saving data...")
        self.save_inventory()
        print("Goodbye!")

def main():
    pos_system = POS()

    while True:
        print("\nPOS System Menu:")
        print("1. List Items")
        print("2. Add Item")
        print("3. Update Item Quantity")
        print("4. Add Customer")
        print("5. Process Sale")
        print("6. Generate Sales Report")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            pos_system.list_items()
        elif choice == '2':
            item_id = input("Enter item ID: ")
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
            pos_system.add_item(item_id, name, price, quantity)
        elif choice == '3':
            item_id = input("Enter item ID: ")
            quantity = int(input("Enter new quantity: "))
            pos_system.update_item_quantity(item_id, quantity)
        elif choice == '4':
            customer_id = input("Enter customer ID: ")
            name = input("Enter customer name: ")
            email = input("Enter customer email: ")
            phone = input("Enter customer phone: ")
            pos_system.add_customer(customer_id, name, email, phone)
        elif choice == '5':
            customer_id = input("Enter customer ID: ")
            items_in_cart = {}
            while True:
                item_id = input("Enter item ID to add to cart (or 'done' to finish): ")
                if item_id.lower() == 'done':
                    break
                quantity = int(input(f"Enter quantity for item {item_id}: "))
                items_in_cart[item_id] = quantity
            pos_system.process_sale(customer_id, items_in_cart)
        elif choice == '6':
            report = pos_system.generate_sales_report()
            print(report)
        elif choice == '7':
            pos_system.exit_system()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
