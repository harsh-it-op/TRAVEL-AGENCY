#!/usr/bin/env python3
"""
Standalone MySQL Connector/Python Demonstration Module for Tourly.
Demonstrates direct database connectivity, parameterized SQL queries,
JOIN operations across Destinations, TourPackages, and Bookings, and
transaction management using `mysql.connector`.

Usage:
    python3 sql/mysql_connector_demo.py
"""
import os
import sys

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    HAS_MYSQL_CONNECTOR = True
except ImportError:
    HAS_MYSQL_CONNECTOR = False


DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DATABASE', 'tourly_db'),
}


def demonstrate_mysql_connector():
    """Connect to MySQL using mysql-connector-python and execute syllabus CRUD + JOIN queries."""
    print("=" * 72)
    print("TOURLY – MySQL Connector/Python Database Connectivity Demonstration")
    print("=" * 72)

    if not HAS_MYSQL_CONNECTOR:
        print("[INFO] `mysql-connector-python` package not installed in current environment.")
        print("Install via: pip install mysql-connector-python")
        return

    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            server_info = connection.get_server_info()
            print(f"[SUCCESS] Connected to MySQL Server version {server_info}")

            cursor = connection.cursor(dictionary=True)

            # 1. Read Destinations by Category
            sql_destinations = """
                SELECT id, name, country, category
                FROM Destinations
                ORDER BY name ASC
                LIMIT 5;
            """
            cursor.execute(sql_destinations)
            rows = cursor.fetchall()
            print("\n--- Top 5 Destinations in MySQL ---")
            for row in rows:
                print(f"  [{row['id']}] {row['name']} ({row['country']}) - Category: {row['category']}")

            # 2. Parameterized INNER JOIN between TourPackages and Destinations
            sql_join = """
                SELECT p.id, p.package_name, d.name AS destination_name,
                       d.category, p.duration, p.price
                FROM TourPackages p
                INNER JOIN Destinations d ON p.destination_id = d.id
                WHERE p.price <= %s
                ORDER BY p.price ASC;
            """
            max_budget = 25000.00
            cursor.execute(sql_join, (max_budget,))
            packages = cursor.fetchall()
            print(f"\n--- Tour Packages Under ₹{max_budget:,.2f} (INNER JOIN Query) ---")
            for pkg in packages:
                print(f"  * {pkg['package_name']} ({pkg['destination_name']}) | {pkg['duration']} | ₹{pkg['price']:,.2f}")

            # 3. Aggregate Booking Statistics
            sql_stats = """
                SELECT booking_status, COUNT(*) AS total_count, SUM(total_price) AS revenue
                FROM Bookings
                GROUP BY booking_status;
            """
            cursor.execute(sql_stats)
            stats = cursor.fetchall()
            print("\n--- Booking Status Summary (GROUP BY Aggregation) ---")
            for s in stats:
                print(f"  Status: {s['booking_status']:<10} | Count: {s['total_count']} | Value: ₹{s['revenue'] or 0:,.2f}")

    except MySQLError as err:
        print(f"[MYSQL CONNECTION NOTICE] Could not reach MySQL daemon at {DB_CONFIG['host']}:{DB_CONFIG['port']}: {err}")
        print("Ensure MySQL Server is running and `sql/schema.sql` has been imported.")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\n[CLOSED] MySQL database connection closed cleanly.")


if __name__ == '__main__':
    demonstrate_mysql_connector()
