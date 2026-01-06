import streamlit as st
import pandas as pd

# SQL Server connector
from services.sql_server import connect_sql_server, fetch_table, fetch_query

# -------------------------------
# Core InsightIQ Pipeline Stubs
# -------------------------------
def run_pipeline(df: pd.DataFrame):
    """
    Main InsightIQ processing pipeline
    """
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("📈 Basic Statistics")
    st.write(df.describe(include="all"))

    st.subheader("🧠 AI Insights (Sample)")
    st.info(
        "Automatically generated business insights will appear here "
        "(KPI detection, summaries, PDF reports, dashboards, etc.)"
    )

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="InsightIQ", layout="wide")

st.title("🚀 InsightIQ – Automated Business Intelligence Platform")
st.caption("No-code analytics pipeline for CSV and SQL data sources")

st.sidebar.header("🔌 Data Source")

source_type = st.sidebar.selectbox(
    "Select data source",
    ["CSV Upload", "SQL Server"]
)

# -------------------------------
# CSV Upload
# -------------------------------
if source_type == "CSV Upload":
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("CSV file loaded successfully")
        run_pipeline(df)

# -------------------------------
# SQL Server Integration
# -------------------------------
elif source_type == "SQL Server":
    st.sidebar.subheader("SQL Server Credentials")

    server = st.sidebar.text_input("Server (hostname or IP)")
    database = st.sidebar.text_input("Database")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    mode = st.sidebar.radio("Query Mode", ["Table", "Custom Query"])

    table_name = ""
    sql_query = ""

    if mode == "Table":
        table_name = st.sidebar.text_input("Table Name")
    else:
        sql_query = st.sidebar.text_area("SQL Query")

    if st.sidebar.button("Load Data"):
        try:
            conn = connect_sql_server(
                server=server,
                database=database,
                username=username,
                password=password
            )

            if mode == "Table":
                df = fetch_table(conn, table_name)
            else:
                df = fetch_query(conn, sql_query)

            st.success("SQL Server data loaded successfully")
            run_pipeline(df)

        except Exception as e:
            st.error(f"Failed to connect or fetch data: {e}")
