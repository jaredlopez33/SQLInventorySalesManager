-- ============================================================================
-- SQL Relational Database Schema & Queries (SQLite)
-- Project: Inventory and Sales Management System
-- Author: Jared Lopez
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. CREATE TABLES (DDL)
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- 2. INSERT SAMPLE DATA (DML - INSERT)
INSERT INTO Products (name, category, price, stock) VALUES
    ('Mechanical Keyboard', 'Electronics', 85.00, 15),
    ('Wireless Mouse', 'Electronics', 35.50, 30),
    ('USB-C Docking Station', 'Accessories', 120.00, 10),
    ('27-inch IPS Monitor', 'Displays', 260.00, 8);

INSERT INTO Customers (full_name, email) VALUES
    ('Ana Torres', 'ana.torres@example.com'),
    ('Carlos Mendoza', 'carlos.mendoza@example.com'),
    ('Lucia Vargas', 'lucia.vargas@example.com');

INSERT INTO Orders (customer_id, product_id, quantity, order_date) VALUES
    (1, 1, 2, '2026-11-10'),
    (2, 2, 3, '2026-11-12'),
    (1, 4, 1, '2026-11-15'),
    (3, 3, 2, '2026-11-17');

-- 3. QUERY DATA (DML - SELECT)
SELECT * FROM Products ORDER BY product_id;
SELECT * FROM Customers ORDER BY customer_id;

-- 4. MODIFY DATA (DML - UPDATE)
UPDATE Products
SET stock = stock - 1, price = 80.00
WHERE product_id = 1;

-- 5. DELETE DATA (DML - DELETE)
DELETE FROM Orders
WHERE order_id = 4;

-- 6. MULTI-TABLE RELATIONAL JOIN (INNER JOIN)
SELECT
    o.order_id,
    o.order_date,
    c.full_name AS customer_name,
    p.name AS product_name,
    o.quantity,
    p.price,
    (o.quantity * p.price) AS line_total
FROM Orders o
INNER JOIN Customers c ON o.customer_id = c.customer_id
INNER JOIN Products p ON o.product_id = p.product_id
ORDER BY o.order_date DESC;

-- 7. AGGREGATE FUNCTIONS (COUNT, SUM, AVG)
SELECT
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS total_units_sold,
    SUM(o.quantity * p.price) AS total_revenue,
    AVG(o.quantity * p.price) AS avg_order_value
FROM Orders o
INNER JOIN Products p ON o.product_id = p.product_id;