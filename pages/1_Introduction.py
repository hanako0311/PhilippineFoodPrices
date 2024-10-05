import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('data/wfp_food_prices_phl.csv', skiprows=1)
    return data

data_cleaned = load_data()

# Introduction page content
st.title("Philippine Food Prices")
st.write("""
This dataset contains food prices data for the Philippines, sourced from the **World Food Programme** Price Database. It includes commodities such as maize, rice, beans, and sugar, with prices updated regularly. The dataset contains data points from 2000 to 2024 across various markets in the Philippines.
""")
st.dataframe(data_cleaned.head())
