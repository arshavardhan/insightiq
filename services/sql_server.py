import pyodbc
import pandas as pd

def connect_sql_server(server, database, username, password,
                       driver="{ODBC Driver 17 for SQL Server}"):
    """
    Establish connection to Microsoft SQL Server
    """
    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    return pyodbc.connect(conn_str)

def fetch_table(conn, table_name):
    """
    Fetch full table from SQL Server
    """
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, conn)

def fetch_query(conn, sql_query):
    """
    Execute custom SQL query
    """
    return pd.read_sql(sql_query, conn)
