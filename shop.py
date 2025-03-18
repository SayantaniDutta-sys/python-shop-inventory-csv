# Program
import csv
from tabulate import tabulate

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self, filename="inventory.csv"):
        self.filename = filename
        self.products = self.load_inventory()

    def load_inventory(self):
        products = {}
        try:
            with open(self.filename, newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    product_id, name, price, quantity = row
                    products[product_id] = Product(product_id, name, float(price), int(quantity))
        except FileNotFoundError:
            pass
        return products

    def save_inventory(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["product_id", "product_name", "price", "quantity"])
            for product in self.products.values():
                writer.writerow([product.product_id, product.name, product.price, product.quantity])

    def add_product(self, product_id, name, price, quantity):
        self.products[product_id] = Product(product_id, name, price, quantity)
        self.save_inventory()

    def update_product(self, product_id, quantity_sold):
        if product_id in self.products:
            self.products[product_id].quantity -= quantity_sold
            self.save_inventory()

    def display_inventory(self):
        table = [[p.product_id, p.name, p.price, p.quantity] for p in self.products.values()]
        print(tabulate(table, headers=["Product ID", "Name", "Price", "Quantity"], tablefmt="grid"))

class Sale:
    def __init__(self, sale_id, product_id, name, quantity_sold, total_price):
        self.sale_id = sale_id
        self.product_id = product_id
        self.name = name
        self.quantity_sold = quantity_sold
        self.total_price = total_price

class SalesManager:
    def __init__(self, filename="sales.csv"):
        self.filename = filename
        self.sales = []

    def record_sale(self, sale):
        self.sales.append(sale)
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([sale.sale_id, sale.product_id, sale.name, sale.quantity_sold, sale.total_price])

    def display_sales(self):
        try:
            with open(self.filename, newline='') as file:
                reader = csv.reader(file)
                next(reader)
                table = [row for row in reader]
                print(tabulate(table, headers=["Sale ID", "Product ID", "Name", "Quantity Sold", "Total Price"], tablefmt="grid"))
        except FileNotFoundError:
            print("No sales records found.")

class ShopSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.sales_manager = SalesManager()

    def menu(self):
        while True:
            print("\n--- Small Shop Management System ---")
            print("1. View Inventory")
            print("2. Add Product to Inventory")
            print("3. Process a Sale")
            print("4. View Sales Report")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.inventory.display_inventory()
            elif choice == "2":
                pid = input("Enter Product ID: ")
                name = input("Enter Product Name: ")
                price = float(input("Enter Price: "))
                quantity = int(input("Enter Quantity: "))
                self.inventory.add_product(pid, name, price, quantity)
            elif choice == "3":
                sale_id = input("Enter Sale ID: ")
                while True:
                    pid = input("Enter Product ID to sell (or 'done' to finish): ")
                    if pid == "done":
                        break
                    if pid in self.inventory.products:
                        qty = int(input(f"Enter quantity for {self.inventory.products[pid].name}: "))
                        if qty <= self.inventory.products[pid].quantity:
                            total = self.inventory.products[pid].price * qty
                            sale = Sale(sale_id, pid, self.inventory.products[pid].name, qty, total)
                            self.sales_manager.record_sale(sale)
                            self.inventory.update_product(pid, qty)
                            print("Sale recorded successfully.")
                        else:
                            print("Insufficient stock!")
                    else:
                        print("Product not found!")
            elif choice == "4":
                self.sales_manager.display_sales()
            elif choice == "5":
                print("Exiting system.")
                break
            else:
                print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    shop = ShopSystem()
    shop.menu()

