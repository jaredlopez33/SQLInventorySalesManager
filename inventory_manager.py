import sqlite3
from datetime import datetime

DB_NAME = "inventory_sales.db"


def get_connection():
    """Creates and returns a SQLite database connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    """Creates the relational tables (Products, Customers, Orders) if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                stock INTEGER NOT NULL CHECK (stock >= 0)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                order_date TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
            );
        """)
        conn.commit()


def seed_sample_data():
    """Populates initial sample records if the Products table is currently empty."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Products;")
        if cursor.fetchone()[0] > 0:
            return

        sample_products = [
            ("Mechanical Keyboard", "Electronics", 85.00, 15),
            ("Wireless Mouse", "Electronics", 35.50, 30),
            ("USB-C Docking Station", "Accessories", 120.00, 10),
            ("27-inch IPS Monitor", "Displays", 260.00, 8),
        ]
        cursor.executemany(
            "INSERT INTO Products (name, category, price, stock) VALUES (?, ?, ?, ?);",
            sample_products,
        )

        sample_customers = [
            ("Ana Torres", "ana.torres@example.com"),
            ("Carlos Mendoza", "carlos.mendoza@example.com"),
            ("Lucia Vargas", "lucia.vargas@example.com"),
        ]
        cursor.executemany(
            "INSERT INTO Customers (full_name, email) VALUES (?, ?);",
            sample_customers,
        )

        sample_orders = [
            (1, 1, 2, "2026-11-10"),
            (2, 2, 3, "2026-11-12"),
            (1, 4, 1, "2026-11-15"),
            (3, 3, 2, "2026-11-17"),
        ]
        cursor.executemany(
            "INSERT INTO Orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?);",
            sample_orders,
        )
        conn.commit()


def add_product():
    """Inserts a new product record into the Products table."""
    print("\n--- Add New Product ---")
    name = input("Product name: ").strip()
    category = input("Category: ").strip()
    try:
        price = float(input("Unit price ($): "))
        stock = int(input("Initial stock quantity: "))
        if price < 0 or stock < 0:
            print("Error: Price and stock must be non-negative.")
            return
    except ValueError:
        print("Error: Invalid numeric input.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Products (name, category, price, stock) VALUES (?, ?, ?, ?);",
            (name, category, price, stock),
        )
        conn.commit()
    print(f"Product '{name}' added successfully.")


def view_products():
    """Queries and displays all records from the Products table."""
    print("\n--- Product Catalog ---")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, name, category, price, stock FROM Products ORDER BY product_id;")
        rows = cursor.fetchall()

    if not rows:
        print("No products found.")
        return

    print(f"{'ID':<4} | {'Name':<24} | {'Category':<14} | {'Price':<10} | {'Stock':<6}")
    print("-" * 68)
    for r in rows:
        print(f"{r[0]:<4} | {r[1]:<24} | {r[2]:<14} | ${r[3]:<9.2f} | {r[4]:<6}")


def update_product_stock():
    """Updates the stock quantity or unit price for an existing product."""
    view_products()
    try:
        product_id = int(input("\nEnter Product ID to update: "))
        new_stock = int(input("Enter new stock quantity: "))
        new_price = float(input("Enter new unit price ($): "))
        if new_stock < 0 or new_price < 0:
            print("Error: Values cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid input.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Products SET stock = ?, price = ? WHERE product_id = ?;",
            (new_stock, new_price, product_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            print("No product found with that ID.")
        else:
            print("Product updated successfully.")


def delete_product():
    """Deletes a product record from the database by its ID."""
    view_products()
    try:
        product_id = int(input("\nEnter Product ID to delete: "))
    except ValueError:
        print("Error: Invalid Product ID.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE product_id = ?;", (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print("No product found with that ID.")
        else:
            print("Product deleted successfully (along with related orders).")


def add_customer():
    """Inserts a new customer record into the Customers table."""
    print("\n--- Register New Customer ---")
    full_name = input("Full name: ").strip()
    email = input("Email address: ").strip()
    if not full_name or not email:
        print("Error: Name and email are required.")
        return

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Customers (full_name, email) VALUES (?, ?);",
                (full_name, email),
            )
            conn.commit()
        print(f"Customer '{full_name}' registered successfully.")
    except sqlite3.IntegrityError:
        print("Error: A customer with that email already exists.")


def view_customers():
    """Queries and displays all customers in the database."""
    print("\n--- Registered Customers ---")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, full_name, email FROM Customers ORDER BY customer_id;")
        rows = cursor.fetchall()

    if not rows:
        print("No customers found.")
        return

    print(f"{'ID':<4} | {'Full Name':<22} | {'Email':<28}")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]:<4} | {r[1]:<22} | {r[2]:<28}")


def create_order():
    """Creates a new order and decrements the corresponding product stock."""
    view_customers()
    view_products()
    try:
        customer_id = int(input("\nEnter Customer ID: "))
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter quantity to purchase: "))
        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            return
    except ValueError:
        print("Error: Invalid numeric input.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT stock, name FROM Products WHERE product_id = ?;", (product_id,))
        product = cursor.fetchone()
        if not product:
            print("Error: Product ID does not exist.")
            return

        current_stock, product_name = product
        if current_stock < quantity:
            print(f"Error: Insufficient stock for '{product_name}' (Available: {current_stock}).")
            return

        cursor.execute("SELECT customer_id FROM Customers WHERE customer_id = ?;", (customer_id,))
        if not cursor.fetchone():
            print("Error: Customer ID does not exist.")
            return

        order_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO Orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?);",
            (customer_id, product_id, quantity, order_date),
        )
        cursor.execute(
            "UPDATE Products SET stock = stock - ? WHERE product_id = ?;",
            (quantity, product_id),
        )
        conn.commit()
    print("Order recorded and inventory stock updated successfully.")


def view_order_history_join():
    """Uses SQL INNER JOIN across Orders, Customers, and Products to display detailed sales."""
    print("\n--- Detailed Order History (INNER JOIN Report) ---")
    query = """
        SELECT
            o.order_id,
            o.order_date,
            c.full_name,
            p.name,
            o.quantity,
            p.price,
            (o.quantity * p.price) AS line_total
        FROM Orders o
        INNER JOIN Customers c ON o.customer_id = c.customer_id
        INNER JOIN Products p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC, o.order_id DESC;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    if not rows:
        print("No orders recorded yet.")
        return

    print(f"{'Order':<6} | {'Date':<10} | {'Customer':<18} | {'Product':<22} | {'Qty':<4} | {'Total':<10}")
    print("-" * 82)
    for r in rows:
        print(f"{r[0]:<6} | {r[1]:<10} | {r[2]:<18} | {r[3]:<22} | {r[4]:<4} | ${r[6]:<9.2f}")


def view_sales_summary_aggregates():
    """Uses SQL aggregate functions (COUNT, SUM, AVG) to summarize sales metrics."""
    print("\n--- Sales & Revenue Summary (SQL Aggregates) ---")
    query = """
        SELECT
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(o.quantity), 0) AS total_units_sold,
            COALESCE(SUM(o.quantity * p.price), 0.0) AS total_revenue,
            COALESCE(AVG(o.quantity * p.price), 0.0) AS avg_order_value
        FROM Orders o
        INNER JOIN Products p ON o.product_id = p.product_id;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        stats = cursor.fetchone()

    print(f"Total Orders Placed : {stats[0]}")
    print(f"Total Units Sold    : {stats[1]}")
    print(f"Total Gross Revenue : ${stats[2]:.2f}")
    print(f"Average Order Value : ${stats[3]:.2f}")


def main():
    """Main interactive console loop for the SQL Inventory & Sales Management System."""
    initialize_database()
    seed_sample_data()

    while True:
        print("\n==============================================")
        print("   SQL Inventory & Sales Management System")
        print("==============================================")
        print("1. View All Products (SELECT)")
        print("2. Add New Product (INSERT)")
        print("3. Update Product Stock & Price (UPDATE)")
        print("4. Delete Product (DELETE)")
        print("5. View All Customers (SELECT)")
        print("6. Register New Customer (INSERT)")
        print("7. Create Customer Order (INSERT + UPDATE)")
        print("8. View Full Order History (INNER JOIN)")
        print("9. View Sales Summary Report (SUM, COUNT, AVG)")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            view_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product_stock()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            view_customers()
        elif choice == "6":
            add_customer()
        elif choice == "7":
            create_order()
        elif choice == "8":
            view_order_history_join()
        elif choice == "9":
            view_sales_summary_aggregates()
        elif choice == "0":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()