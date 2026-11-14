
import streamlit as st

from database import get_schema, run_select_query

st.set_page_config(
    page_title="AI SQL Data Analyst",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI SQL Data Analyst Agent")
st.write("Explore your sales database using SQL.")

# Display database connection status
try:
    schema = get_schema()
    st.success("Connected to the sales database!")
except Exception as error:
    st.error(f"Database connection failed: {error}")
    st.stop()

# Display database schema
with st.expander("View database schema"):
    for table_name, columns in schema.items():
        st.markdown(f"**Table: {table_name}**")
        st.write(", ".join(
            f"{column['name']} ({column['type']})"
            for column in columns
        ))

# Example questions
question = st.selectbox(
    "Choose a question to explore:",
    [
        "What is the total revenue?",
        "Show the top 5 products by revenue",
        "Show monthly revenue for 2025",
        "Show all customers",
    ],
)

queries = {
    "What is the total revenue?": """
        SELECT SUM(amount) AS total_revenue
        FROM orders
    """,
    "Show the top 5 products by revenue": """
        SELECT
            p.product_name,
            SUM(o.amount) AS revenue
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 5
    """,
    "Show monthly revenue for 2025": """
        SELECT
            SUBSTR(order_date, 1, 7) AS month,
            SUM(amount) AS revenue
        FROM orders
        WHERE order_date >= '2025-01-01'
          AND order_date < '2026-01-01'
        GROUP BY SUBSTR(order_date, 1, 7)
        ORDER BY month
    """,
    "Show all customers": """
        SELECT *
        FROM customers
        ORDER BY customer_id
    """,
}

if st.button("Run SQL query", type="primary"):
    sql = queries[question]

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    try:
        results = run_select_query(sql)

        st.subheader("Query results")
        st.dataframe(results, use_container_width=True)

        if question == "What is the total revenue?":
            revenue = results["total_revenue"].iloc[0]
            st.metric(
                "Total Revenue",
                f"₹{revenue:,.2f}" if revenue is not None else "₹0.00",
            )

        if question == "Show monthly revenue for 2025":
            st.subheader("Monthly Revenue Trend")
            st.line_chart(
                results.set_index("month")["revenue"]
            )

    except Exception as error:
        st.error(f"Query execution failed: {error}")
