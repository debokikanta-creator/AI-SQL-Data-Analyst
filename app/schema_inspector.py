
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "sales.db"


def get_database_schema():

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    connection = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True
    )

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, type
            FROM sqlite_master
            WHERE type IN ('table', 'view')
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        objects = cursor.fetchall()

        schema = []

        for name, object_type in objects:

            cursor.execute(
                f'PRAGMA table_info("{name}")'
            )

            columns = cursor.fetchall()

            schema.append(
                f"\n{object_type.upper()}: {name}"
            )

            for column in columns:
                column_name = column[1]
                column_type = column[2]

                schema.append(
                    f"- {column_name} ({column_type})"
                )

        return "\n".join(schema)

    finally:
        connection.close()
