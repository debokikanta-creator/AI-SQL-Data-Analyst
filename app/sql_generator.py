
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import date

from schema_inspector import get_database_schema


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


client = OpenAI(
    base_url=os.getenv("LOCAL_AI_BASE_URL"),
    api_key="lm-studio"
)

model = os.getenv("LOCAL_AI_MODEL")


def generate_sql(
    question: str,
    start_date=None,
    end_date=None
) -> str:

    # Automatically discover database schema
    schema = get_database_schema()

    # Build date filtering instructions
    date_instruction = ""

    if start_date is not None and end_date is not None:

        start_date = date.fromisoformat(str(start_date))
        end_date = date.fromisoformat(str(end_date))

        if start_date > end_date:
            raise ValueError(
                "Start date cannot be after end date."
            )

        date_instruction = f"""
IMPORTANT DATE FILTER:

The user selected this date range:

Start Date: {start_date}
End Date: {end_date}

You MUST restrict all order-related calculations
to this date range.

Use the orders.order_date column.

Apply this condition:

date(o.order_date) BETWEEN
date('{start_date}') AND date('{end_date}')

If the orders table has no alias, use:

date(orders.order_date) BETWEEN
date('{start_date}') AND date('{end_date}')

If an alias is used for orders, use that alias
consistently.

Include the date condition in the appropriate
WHERE clause.

Do not calculate results using orders outside
the selected date range.
"""

    prompt = f"""
You are an expert SQLite SQL developer.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

{date_instruction}

RULES:

1. Generate valid SQLite SQL.
2. Use only tables and columns in the schema.
3. Use JOIN when information requires multiple tables.
4. Use GROUP BY with aggregate queries.
5. Use SUM(column), COUNT(*), AVG(column),
   MIN(column), and MAX(column) correctly.
6. Never use aggregate functions in WHERE.
7. Use HAVING for aggregate filtering.
8. Use ORDER BY for rankings.
9. Use LIMIT for top-N questions.
10. Generate SELECT statements only.
11. Generate exactly one SQL statement.
12. Never invent table or column names.
13. Return SQL only, without Markdown.
14. Follow the selected date range whenever provided.

Generate the SQL for the user's question.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=500
    )

    sql = response.choices[0].message.content.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "", 1)
        sql = sql.replace("```", "").strip()

    return sql
