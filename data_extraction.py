import psycopg2
import pandas as pd

def get_connection():
    return psycopg2.connect(
    dbname="supermarket_analysis",
    user="postgres",
    password="1108",
    host="localhost",
    port="5432"
    )

def extract_product_sales_data():
    conn = get_connection()
    query = """
        SELECT product_name, SUM(quantity) as total_sales
        FROM Purchases p
        JOIN Products pr ON p.product_id = pr.product_id
        GROUP BY product_name
        ORDER BY total_sales DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def extract_customer_visit_patterns_data():
    conn = get_connection()
    query = """
        SELECT visit_id, section_id, sequence_number
        FROM Customer_Path
        ORDER BY visit_id, sequence_number
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
def extract_frequent_visit_patterns(n=10):
    conn = get_connection()
    query = """
    SELECT v.visit_id, STRING_AGG(s.section_name, '->' ORDER BY cp.sequence_number) AS path
    FROM Visits v
    JOIN Customer_Path cp ON v.visit_id = cp.visit_id
    JOIN Sections s ON cp.section_id = s.section_id
    GROUP BY v.visit_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    path_counts = df['path'].value_counts().reset_index()
    path_counts.columns = ['path', 'count']
    
    
    top_paths = path_counts.head(n)
    
    return top_paths

def extract_impulse_purchases_data():
    conn = get_connection()
    query = """
        SELECT section_name, COUNT(DISTINCT p.purchase_id) as impulse_purchases
        FROM Sections s
        JOIN Interactions i ON s.section_id = i.section_id
        LEFT JOIN Purchases p ON i.visit_id = p.visit_id AND i.product_id = p.product_id
        JOIN Visits v ON i.visit_id = v.visit_id
        WHERE p.purchase_id IS NOT NULL AND i.interaction_time - v.entry_time < INTERVAL '10 minutes'
        GROUP BY section_name
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def extract_popular_sections_data():
    conn = get_connection()
    query = """
        SELECT section_name, COUNT(DISTINCT visit_id) as visit_count
        FROM Customer_Path cp
        JOIN Sections s ON cp.section_id = s.section_id
        GROUP BY section_name
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def extract_queue_wait_times_data():
    conn = get_connection()
    query = """
        SELECT visit_id, wait_duration
        FROM Queue_Wait_Times
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
