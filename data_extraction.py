import psycopg2
import pandas as pd

def get_connection():
    conn = psycopg2.connect(
        dbname="customer_analysis",
    user="postgres",
    password="1108",
    host="localhost",
    port="5432"
    )
    return conn

def extract_customer_demographics():
    conn = get_connection()
    
    query = """
        SELECT age, gender
        FROM Customers
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def extract_store_heatmap():
    conn = get_connection()
    
    query = """
        SELECT s.section_name, COUNT(v.visit_id) as visit_count
        FROM Sections s
        JOIN Customer_Path cp ON s.section_id = cp.section_id
        JOIN Visits v ON cp.visit_id = v.visit_id
        GROUP BY s.section_name
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df
