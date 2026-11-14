
import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "sales.db"


def get_connection():
    """Open a connection to the local sales database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA query_only = ON")
    return connection


def get_schema():
    """Return the database tables and their columns."""
    with get_connection() as connection:
        tables = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()

        schema = {}

        for table in tables:
            table_name = table["name"]

            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()

            schema[table_name] = [
                {
                    "name": column["name"],
                    "type": column["type"],
                }
                for column in columns
            ]

        return schema


def run_select_query(sql, params=()):
    """Execute a read-only SELECT query with optional parameters."""

    normalized = sql.lstrip().upper()

    if not normalized.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    with get_connection() as connection:
        cursor = connection.execute(sql, params)
        rows = cursor.fetchmany(1000)
        columns = [item[0] for item in cursor.description]

    return pd.DataFrame(
        [dict(zip(columns, row)) for row in rows],
        columns=columns,
    )


def get_dashboard_kpis(start_date, end_date):
    """Calculate KPIs within the selected date range."""

    query = """
        SELECT
            COALESCE(SUM(amount), 0) AS total_revenue,
            COUNT(*) AS total_orders,
            COUNT(DISTINCT customer_id) AS total_customers,
            COALESCE(AVG(amount), 0) AS average_order_value
        FROM orders
        WHERE date(order_date) BETWEEN date(?) AND date(?)
    """

    params = (start_date, end_date)

    return run_select_query(query, params).iloc[0].to_dict()


def get_revenue_by_product(start_date, end_date):
    """Calculate product revenue within the selected date range."""

    query = """
        SELECT
            p.product_name,
            SUM(o.amount) AS revenue
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        WHERE date(o.order_date) BETWEEN date(?) AND date(?)
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 10
    """

    params = (start_date, end_date)

    return run_select_query(query, params)


def get_revenue_by_category(start_date, end_date):
    """Calculate category revenue within the selected date range."""

    query = """
        SELECT
            p.category,
            SUM(o.amount) AS revenue
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        WHERE date(o.order_date) BETWEEN date(?) AND date(?)
        GROUP BY p.category
        ORDER BY revenue DESC
    """

    params = (start_date, end_date)

    return run_select_query(query, params)
