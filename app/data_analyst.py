
from pathlib import Path
import pandas as pd

from sql_generator import generate_sql
from sql_validator import execute_sql


# Locate the existing SQLite database
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "data" / "sales.db"


def analyze_question(
    question: str,
    start_date=None,
    end_date=None
):
    """
    Convert a natural language question into SQL,
    validate it, execute it, and return the results.
    """

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    print("Generating SQL using local AI...")

    # Step 1: Generate SQL with optional date range
    sql = generate_sql(
        question,
        start_date,
        end_date
    )

    print("\nGenerated SQL:")
    print(sql)

    # Step 2: Validate and execute SQL
    print("\nValidating and executing SQL...")

    columns, rows = execute_sql(
        str(DB_PATH),
        sql
    )

    # Step 3: Convert results to DataFrame
    dataframe = pd.DataFrame(
        rows,
        columns=columns
    )

    return sql, dataframe
