import pandas as pd
import streamlit as st

# Access the cached data from session_state
df = st.session_state["df"]

# Introduction page content
st.title("Philippine Food Prices Data Exploration")
st.write(
    """
## Overview
Welcome to the **Philippine Food Prices Dashboard**. This interactive dashboard provides an opportunity to explore and analyze the **food price trends** in the Philippines from **2000 to 2024**. Sourced from the **World Food Programme** Price Database, the data covers key commodities like **maize, rice, beans, sugar**, and more, across various regions and markets in the country.

## Purpose
This dashboard aims to help users interpret and gain insights into:
- **Price Trends Over Time**: Understand how food prices have evolved from 2000 to 2024, including the impact of key events such as economic fluctuations.
- **Regional Price Variations**: Explore how prices differ across regions in the Philippines, offering a look at regional disparities in food affordability.
- **Retail vs Wholesale Pricing**: Compare retail and wholesale prices to observe differences in pricing strategies across commodities.

Whether you're looking for trends, comparing regions, or analyzing the effects of market conditions on food prices, this dashboard allows you to gain a deeper understanding of the data.

## Data Details
Here are the details of the dataset:
- **Date Range**: 2000 to 2024
- **Regions Covered**: Markets across various regions in the Philippines
- **Commodities**: Includes maize, rice, beans, sugar, meat, fish, vegetables, and more
- **Price Type**: Both **retail** and **wholesale** prices are available
- **Currency**: Prices are available in **Philippine Peso (PHP)** and **US Dollar (USD)**

## How to Use This Dashboard
You can use the filters on the left-hand sidebar to select specific **regions** and **commodities** of interest. The visualizations provided in the dashboard will help you explore:
- **Key metrics** such as total, average, and median prices
- **Trends in pricing over time**
- **Price variations across different regions and markets**

"""
)

# Display first few rows of the dataset
st.write("### Sample of the Dataset:")
st.dataframe(df.head())

# Additional information or instructions
st.write(
    """
### Next Steps
Use the **filters in the sidebar** to explore the data further. Choose specific regions, commodities, and price types to gain insights into pricing trends and regional disparities.
The visualizations will update dynamically based on your selections, allowing you to interpret the data in real-time.
"""
)
