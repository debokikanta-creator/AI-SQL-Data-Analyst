
from pathlib import Path

from sql_validator import validate_sql, execute_sql


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "sales.db"


def test_valid_select():
    sql = "SELECT SUM(amount) FROM orders"

    assert validate_sql(sql)
    print("PASS: SELECT query accepted")


def test_valid_cte():
    sql = """
    WITH revenue AS (
        SELECT SUM(amount) AS total
        FROM orders
    )
    SELECT total FROM revenue
    """

    assert validate_sql(sql)
    print("PASS: CTE query accepted")


def test_invalid_delete():
    try:
        validate_sql("DELETE FROM orders")
        raise AssertionError("DELETE was accepted")
    except ValueError:
        print("PASS: DELETE query rejected")


def test_multiple_statements():
    try:
        validate_sql(
            "SELECT * FROM orders; DROP TABLE orders;"
        )
        raise AssertionError("Multiple statements accepted")
    except ValueError:
        print("PASS: Multiple statements rejected")


def test_database_execution():
    columns, rows = execute_sql(
        str(DB_PATH),
        "SELECT SUM(amount) AS revenue FROM orders"
    )

    assert "revenue" in columns
    assert len(rows) == 1

    print("PASS: Database query executed")


if __name__ == "__main__":
    test_valid_select()
    test_valid_cte()
    test_invalid_delete()
    test_multiple_statements()
    test_database_execution()

    print("\nAll SQL validator tests passed!")
