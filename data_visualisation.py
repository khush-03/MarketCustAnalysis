import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
from data_extraction import (
    extract_product_sales_data,
    extract_customer_visit_patterns_data,
    extract_impulse_purchases_data,
    extract_popular_sections_data,
    extract_queue_wait_times_data,
    extract_frequent_visit_patterns
    
)
def plot_frequent_visit_patterns():
    data = extract_frequent_visit_patterns(n=10)  
    
    paths = data['path'].tolist()
    counts = data['count'].tolist()
    
    sources = []
    targets = []
    values = []
    
    label_list = []
    for path in paths:
        sections = path.split('->')
        for i in range(len(sections) - 1):
            sources.append(sections[i])
            targets.append(sections[i + 1])
            values.append(counts[paths.index(path)])
            if sections[i] not in label_list:
                label_list.append(sections[i])
            if sections[i + 1] not in label_list:
                label_list.append(sections[i + 1])
    
    source_indices = [label_list.index(source) for source in sources]
    target_indices = [label_list.index(target) for target in targets]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label_list,
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values
        ))])
    
    fig.update_layout(title_text="Most Frequent Customer Visit Patterns", font_size=10)
    st.plotly_chart(fig)
    
def plot_product_sales():
    data = extract_product_sales_data()
    st.bar_chart(data.set_index('product_name')['total_sales'])

def plot_customer_visit_patterns():
    data = extract_customer_visit_patterns_data()

    data = data.head(10)  

    # Create Sankey diagram data
    sources = []
    targets = []
    values = []

    for i in range(len(data) - 1):
        if data.iloc[i]['visit_id'] == data.iloc[i + 1]['visit_id']:
            sources.append(data.iloc[i]['section_id'])
            targets.append(data.iloc[i + 1]['section_id'])
            values.append(1)

    label_list = list(pd.unique(data[['section_id']].values.ravel('K')))
    label_list.sort()
    labels = [str(label) for label in label_list]

    source_indices = [labels.index(str(source)) for source in sources]
    target_indices = [labels.index(str(target)) for target in targets]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values
        ))])

    fig.update_layout(title_text="Customer Visit Patterns", font_size=10)
    st.plotly_chart(fig)



def plot_impulse_purchases():
    data = extract_impulse_purchases_data()
    
    pivot_data = data.pivot_table(index='section_name', values='impulse_purchases')

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_data, annot=True, cmap="coolwarm", cbar_kws={'label': ''})
    plt.title("Impulse Purchases by Section")
    plt.xlabel("Impulse Purchases")
    plt.ylabel("Section Name")
    st.pyplot(plt)
    
def plot_popular_sections():
    data = extract_popular_sections_data()
    fig, ax = plt.subplots()
    ax.pie(data['visit_count'], labels=data['section_name'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

def plot_queue_wait_times():
    data = extract_queue_wait_times_data()
    st.line_chart(data.set_index('visit_id')['wait_duration'])

def view_insights():
    st.title("Supermarket Customer Insights Dashboard")
    
    st.sidebar.subheader("Select Visualization")
    options = ["Product Sales", "Customer Visit Patterns", "Impulse Purchases", "Popular Sections", "Queue Wait Times", "Customer pattern"]
    choice = st.sidebar.selectbox("Choose a metric to visualize", options)
    
    if choice == "Product Sales":
        st.header("Product Sales Analysis")
        plot_product_sales()
    elif choice == "Customer Visit Patterns":
        st.header("Customer Visit Patterns")
        plot_customer_visit_patterns()
    elif choice == "Impulse Purchases":
        st.header("Impulse Purchases")
        plot_impulse_purchases()
    elif choice == "Popular Sections":
        st.header("Popular Sections")
        plot_popular_sections()
    elif choice == "Queue Wait Times":
        st.header("Queue Wait Times")
        plot_queue_wait_times()
    elif choice == "Customer pattern":
        st.header("Customer pattern")
        plot_frequent_visit_patterns()
