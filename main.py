import streamlit as st
from data_visualisation import view_insights

def main():
    st.sidebar.title("Supermarket Analysis Dashboard")
    selection = st.sidebar.radio("Go to", ["View Insights"])
    
    if selection == "View Insights":
        view_insights()

if __name__ == "__main__":
    main()
