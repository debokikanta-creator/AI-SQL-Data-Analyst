
import streamlit as st
import sys
from pathlib import Path

# Make project modules accessible
APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))

from data_analyst import analyze_question
from database import (
    get_dashboard_kpis,
    get_revenue_by_product,
    get_revenue_by_category
)
from insights import explain_results

# Page configuration
st.set_page_config(
    page_title="AI SQL Data Analyst",
    page_icon="📊",
    layout="wide"
)

# Application heading
st.title("📊 AI SQL Data Analyst")
st.caption(
    "Ask questions about your sales database "
    "using your local Qwen AI model."
)

st.success("Local AI connected through LM Studio")
st.divider()

st.subheader("📅 Filter Data by Date")

# Get available dates from database
from database import get_connection

with get_connection() as connection:
    date_range = connection.execute("""
        SELECT
            MIN(order_date),
            MAX(order_date)
        FROM orders
    """).fetchone()

min_date = date_range[0]
max_date = date_range[1]

st.write(f"Available dates: {min_date} to {max_date}")
from datetime import date

# Convert database dates
min_date = date.fromisoformat(min_date)
max_date = date.fromisoformat(max_date)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

if start_date > end_date:
    st.error("Start date cannot be after end date.")
else:
    st.success(
        f"Selected period: {start_date} to {end_date}"
    )

# ==========================================
# PHASE 18: BUSINESS KPI DASHBOARD
# ==========================================

st.divider()
st.header("📊 Business Performance Dashboard")

try:
    kpis = get_dashboard_kpis(
    start_date,
    end_date
    )

    # Four KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Revenue",
        f"{kpis['total_revenue']:,.2f}"
    )

    col2.metric(
        "📦 Total Orders",
        f"{kpis['total_orders']:,}"
    )

    col3.metric(
        "👥 Total Customers",
        f"{kpis['total_customers']:,}"
    )

    col4.metric(
        "🧾 Average Order Value",
        f"{kpis['average_order_value']:,.2f}"
    )

    st.divider()

    # Revenue by product
    st.subheader("🏆 Revenue by Product")

    product_data = get_revenue_by_product(
    start_date,
    end_date
    )

    if not product_data.empty:
        product_chart = product_data.set_index(
            "product_name"
        )

        st.bar_chart(product_chart["revenue"])
    else:
        st.info("No product revenue data available.")

    # Revenue by category
    st.subheader("📂 Revenue by Category")

    category_data = get_revenue_by_category(
    start_date,
    end_date
    )

    if not category_data.empty:
        category_chart = category_data.set_index(
            "category"
        )

        st.bar_chart(category_chart["revenue"])
    else:
        st.info("No category revenue data available.")

except Exception as dashboard_error:
    st.error(
        f"Dashboard could not load: {dashboard_error}"
    )

st.divider()


# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write("AI Model: Qwen3 4B")
    st.write("Database: SQLite")
    st.write("AI Runtime: LM Studio")
    st.success("No cloud API required")

# Example questions
st.subheader("💬 Ask your database")

examples = [
    "What is the total revenue?",
    "Which products generate the highest revenue?",
    "How many orders are there?",
    "What are the top 5 products by sales?"
]

selected_question = st.selectbox(
    "Choose an example question",
    [""] + examples
)

question = st.text_input(
    "Enter your question:",
    value=selected_question,
    placeholder="Example: What is the total revenue?"
)

# Run analysis
if st.button("🚀 Analyze Data", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner(
            "Qwen AI is generating and executing SQL..."
        ):
            try:
                sql, results = analyze_question(question, start_date, end_date)

                st.subheader("🧠 Generated SQL")

                st.code(sql, language="sql")

                st.subheader("📊 Query Results")

                st.dataframe(
                    results,
                    use_container_width=True
                )

                st.metric(
                    "Rows returned",
                    len(results)
                )
                
                st.subheader("🧠 AI Analysis & Insights")

                try:
                    with st.spinner("Qwen3 is analyzing your results..."):
                        explanation = explain_results(question,sql,results)

                    st.info(explanation)

                except Exception as explanation_error:
                    st.warning(
                    f"Could not generate AI explanation: "
                    f"{explanation_error}"
                    )

                # Simple chart when suitable
                numeric_columns = results.select_dtypes(
                    include="number"
                ).columns.tolist()

                if len(results) > 1 and numeric_columns:
                    st.subheader("📈 Data Visualization")

                    st.bar_chart(
                        results.set_index(
                            results.columns[0]
                        )[numeric_columns]
                    )

                st.success("Analysis completed successfully!")

            except Exception as error:
                st.error(f"Analysis failed: {error}")

st.divider()

st.caption(
    "Powered by local Qwen3 AI | "
    "LM Studio | Python | SQLite | Streamlit"
)
