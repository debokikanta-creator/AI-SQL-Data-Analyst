
import re
import sqlite3


def validate_sql(sql: str) -> bool:
    """Allow only one read-only SELECT or WITH statement."""

    if not sql or not sql.strip():
        raise ValueError("SQL query is empty.")

    cleaned = sql.strip()

    # Remove SQL comments for initial statement inspection
    cleaned = re.sub(r"/\*.*?\*/", " ", cleaned, flags=re.S)
    cleaned = re.sub(r"--[^\r\n]*", " ", cleaned)

    # Remove optional trailing semicolon
    cleaned = cleaned.rstrip().rstrip(";").strip()

    if not cleaned:
        raise ValueError("SQL query is empty.")

    # Reject multiple statements
    if ";" in cleaned:
        raise ValueError("Multiple SQL statements are not allowed.")

    # Allow only SELECT and WITH statements
    if not re.match(r"^(SELECT|WITH)\b", cleaned, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")

    # Block dangerous SQL operations
    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|"
        r"REPLACE|ATTACH|DETACH|PRAGMA)\b",
        re.IGNORECASE
    )

    if forbidden.search(cleaned):
        raise ValueError("Unsafe SQL operation detected.")

    return True


def execute_sql(db_path: str, sql: str):
    """Execute SQL using SQLite read-only mode and authorization."""

    validate_sql(sql)

    connection = sqlite3.connect(
        f"file:{db_path}?mode=ro",
        uri=True,
        timeout=10
    )

    # Additional SQLite-level protection
    connection.execute("PRAGMA query_only = ON")

    def authorize(action, arg1, arg2, database, trigger):
        allowed = {
            sqlite3.SQLITE_SELECT,
            sqlite3.SQLITE_READ,
            sqlite3.SQLITE_FUNCTION,
        }

        if action not in allowed:
            return sqlite3.SQLITE_DENY

        # Prevent extension loading
        if action == sqlite3.SQLITE_FUNCTION:
            function_name = (arg2 or arg1 or "").lower()

            if function_name == "load_extension":
                return sqlite3.SQLITE_DENY

        return sqlite3.SQLITE_OK

    try:
        connection.set_authorizer(authorize)

        cursor = connection.cursor()
        cursor.execute(sql)

        columns = [item[0] for item in cursor.description]

        # Limit returned rows
        rows = cursor.fetchmany(1000)

        return columns, rows

    finally:
        connection.close()
