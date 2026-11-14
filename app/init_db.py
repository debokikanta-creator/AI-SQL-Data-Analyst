
import sqlite3
from pathlib import Path

# Store the database in the project's data folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "sales.db"


def initialize_database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create the customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            city TEXT NOT NULL,
            region TEXT NOT NULL
        )
    """)

    # Create the products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Create the orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id),
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    # Insert sample customers
    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        (customer_id, customer_name, city, region)
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Aarav Sharma", "Kolkata", "East"),
        (2, "Priya Das", "Delhi", "North"),
        (3, "Rahul Verma", "Mumbai", "West"),
        (4, "Ananya Roy", "Bengaluru", "South"),
        (5, "Vikram Singh", "Kolkata", "East"),
    ])

    # Insert sample products
    cursor.executemany("""
        INSERT OR IGNORE INTO products
        (product_id, product_name, category, price)
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Laptop", "Electronics", 55000),
        (2, "Phone", "Electronics", 25000),
        (3, "Office Chair", "Furniture", 8000),
        (4, "Desk", "Furniture", 12000),
        (5, "Headphones", "Accessories", 3000),
    ])

    # Insert sample orders
    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, product_id,
         order_date, quantity, amount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, 1, 1, "2025-01-15", 1, 55000),
        (2, 2, 2, "2025-02-10", 2, 50000),
        (3, 3, 3, "2025-03-05", 3, 24000),
        (4, 4, 4, "2025-04-20", 2, 24000),
        (5, 5, 5, "2025-05-12", 4, 12000),
        (6, 1, 2, "2025-06-18", 1, 25000),
        (7, 2, 1, "2025-07-22", 2, 110000),
        (8, 3, 5, "2025-08-09", 2, 6000),
        (9, 4, 3, "2025-09-14", 1, 8000),
        (10, 5, 4, "2025-10-02", 3, 36000),
        (11, 1, 5, "2025-11-11", 3, 9000),
        (12, 2, 2, "2025-12-05", 1, 25000),
    ])

    connection.commit()
    connection.close()

    print(f"Database created successfully: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()
