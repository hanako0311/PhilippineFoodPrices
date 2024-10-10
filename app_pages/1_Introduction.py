import pandas as pd
import streamlit as st

# Access the cached data from session_state
df = st.session_state["df"]

# Introduction page content
st.title("Philippine Food Prices Data Exploration")
st.write(
    """
## Overview
Welcome to the **Philippine Food Prices Dashboard**, an interactive tool designed to provide an in-depth analysis of **food price trends** in the Philippines from **2000 to 2024**. This dashboard utilizes data sourced from the **World Food Programme (WFP) Price Database**, which tracks key food commodities across various markets in the country.
 
## Purpose of Exploration
The fluctuations in food prices are a critical issue in the Philippines, where a large part of the population is affected by changes in food affordability. Our goal with this data exploration is to uncover insights regarding:
- **Regional disparities in food prices**.
- **Price behavior over time** for various food commodities.
- The differences between **retail** and **wholesale** prices.
 
By analyzing these trends, we aim to provide valuable insights that could inform **policymakers**, **market analysts**, and **consumers** about the factors driving food price changes in the Philippines, ultimately supporting better decision-making and planning.
 
## Features of the Dashboard
This dashboard allows you to:
- **Filter by Region and Commodity**: Select specific regions or commodities to focus your analysis.
- **Key Metrics**: View **average**, and **median** prices of commodities across the dataset.
- **Retail vs Wholesale Price Comparison**: Analyze the differences between retail and wholesale prices.
- **Top 5**: Discover which commodities have the highest and lowest average prices.
- **Price Trends Over Time**: Visualize how prices have changed yearly.
 
## Descriptive Statistics
In addition to visual exploration, the dashboard provides **descriptive statistics** for deeper insight into the dataset. This includes:
- **Percentiles and Summary**: Understand how prices are distributed with percentile-based summaries (25th, 50th, 75th, and 100th).
- **Price Distribution**: A **box plot** highlights how prices vary across the dataset, helping to identify trends and outliers.
- **Categorical Analysis**: Review the frequency distribution of regions, commodities, and food types with dynamic bar or pie charts.
"""
)

# Separator line to distinguish the introduction from user instructions
st.write("---")

# Additional instructions for users
st.write(
    """
### How to Use This Dashboard
To begin exploring, use the **filters on the sidebar** to choose specific regions and commodities. The interactive charts and statistics will update automatically, allowing you to uncover key insights and trends in real-time.
 
### Sample of the Dataset:
Below is a sample preview of the dataset used for this exploration:
"""
)

# Display first few rows of the dataset
st.dataframe(df.head())

# Additional instructions for users
st.write(
    """
### Next Steps
Start exploring by using the **filters in the sidebar**. Navigate through the sections to review **descriptive statistics**, **price trends**, and **commodity comparisons**.
"""
)
