import streamlit as st
import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="customer_analysis",
    user="postgres",
    password="1108",
    host="localhost",
    port="5432"
)

# Function to extract data
def extract_data(query):
    return pd.read_sql_query(query, conn)

# Page setup
st.set_page_config(page_title="Supermarket Customer Insights", layout="wide")
st.title("Supermarket Customer Insights Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
season_filter = st.sidebar.multiselect("Season", options=["Winter", "Spring", "Summer", "Autumn"], default=["Winter", "Spring", "Summer", "Autumn"])
time_range = st.sidebar.slider("Select time range (in minutes)", 0, 60, (0, 60))

# Generate Visit Frequency by Section Heatmap
st.subheader("Visit Frequency by Section")
visit_query = f"""
SELECT section_name, COUNT(*) AS visit_count
FROM Sections s
JOIN Customer_Path cp ON s.section_id = cp.section_id
JOIN Visits v ON cp.visit_id = v.visit_id
WHERE v.season IN ({', '.join([f"'{season}'" for season in season_filter])})
GROUP BY section_name
"""
visit_data = extract_data(visit_query)

fig, ax = plt.subplots()
pivot_data = visit_data.pivot_table(values="visit_count", index="section_name", aggfunc='sum')
sns.heatmap(pivot_data, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Generate Impulse Purchase Heatmap
st.subheader("Impulse Purchase by Section")
impulse_query = f"""
SELECT s.section_name, COUNT(DISTINCT p.purchase_id) as impulse_purchases
FROM Sections s
JOIN Interactions i ON s.section_id = i.section_id
LEFT JOIN Purchases p ON i.visit_id = p.visit_id AND i.product_id = p.product_id
JOIN Visits v ON v.visit_id = i.visit_id
WHERE p.purchase_id IS NOT NULL AND EXTRACT(EPOCH FROM (i.interaction_time - v.entry_time))/60 < {time_range[1]}
AND v.season IN ({', '.join([f"'{season}'" for season in season_filter])})
GROUP BY s.section_name
"""
impulse_data = extract_data(impulse_query)

fig2, ax2 = plt.subplots()
pivot_data2 = impulse_data.pivot_table(values="impulse_purchases", index="section_name", aggfunc='sum')
sns.heatmap(pivot_data2, annot=True, cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# Close the connection
conn.close()
