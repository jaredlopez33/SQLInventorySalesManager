# Overview

As a software engineer continuously expanding my technical skill set, I am focused on mastering relational database design, data integrity constraints, and SQL querying to build reliable, data-driven applications from the ground up.

This software is a console-based **Inventory and Sales Management System** that integrates with a **SQLite** relational database (`inventory_sales.db`) to persist product catalogs, customer records, and sales orders. To use the program, run `inventory_manager.py` from the terminal and choose options from the interactive menu to view or add products (`SELECT` / `INSERT`), update inventory stock and prices (`UPDATE`), delete records (`DELETE`), register customers, place orders that automatically decrement stock, view detailed order histories via `INNER JOIN`, and generate sales summaries using `COUNT`, `SUM`, and `AVG`.

My purpose for writing this software was to practice structuring related database tables with primary and foreign keys, writing safe parameterized SQL statements, and combining relational joins with aggregate functions for practical reporting.

[Software Demo Video](https://drive.google.com/file/d/1aYBLn8aFWGsBPG9Y1tCJ9uU4KGlFAJFk/view?usp=sharing)

# Relational Database

This project uses **SQLite** (`inventory_sales.db`), a lightweight, serverless relational database engine that stores data locally in a single file and enforces foreign key constraints when `PRAGMA foreign_keys = ON;` is enabled.

The database consists of three related tables:
- **`Products`**: Stores `product_id` (primary key, auto-incrementing), `name`, `category`, `price` (non-negative), and `stock` (non-negative).
- **`Customers`**: Stores `customer_id` (primary key, auto-incrementing), `full_name`, and `email` (unique).
- **`Orders`**: Stores `order_id` (primary key, auto-incrementing), `customer_id` (foreign key referencing `Customers.customer_id`), `product_id` (foreign key referencing `Products.product_id`), `quantity` (positive integer), and `order_date`.

# Development Environment

I used **Visual Studio Code** as my code editor along with the **SQLite Viewer** extension to inspect the database tables visually, and **Git** and **GitHub** to manage and publish the source code.

The application is written in **Python 3** using the built-in `sqlite3` library for connecting to SQLite and executing SQL queries, along with the standard `datetime` module for recording order dates.

# Useful Websites

- [SQLite Official Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3 Module Documentation](https://docs.python.org/3/library/sqlite3.html)

# Future Work

- Add low-stock alerts and export sales summary reports to CSV files.
- Add database indexes on foreign key columns to improve query performance on larger datasets.
- Add an option to update or cancel existing orders while accurately restoring product stock.