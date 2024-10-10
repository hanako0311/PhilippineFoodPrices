import streamlit as st

# Conclusion page content
st.markdown(
    """
## Summary of Insights
Our analysis of **Philippine Food Prices** from 2000 to 2024 has revealed key insights into regional disparities, commodity-specific behaviors, and price trends over time. The interactive dashboard allowed us to explore the following:

- **Price Distribution**: The data shows that most commodities are priced lower, but certain commodities like seafood and meat stand out as higher-priced outliers. The distribution varies significantly depending on the regions selected.
- **Regional Price Variations**: There is considerable variation in prices between regions. Regions with limited infrastructure or market access tend to have higher prices, particularly for certain commodities like vegetables and fruits. This highlights potential areas where market interventions could help stabilize prices.
- **Retail vs Wholesale Price Differences**: A clear difference in pricing between retail and wholesale markets was observed, with retail prices generally being higher, as expected. This insight is particularly valuable for policymakers and market analysts aiming to understand supply chain dynamics.
- **Price Trends Over Time**: Price trends, whether viewed daily, monthly, quarterly, or yearly, indicate that fluctuations are more pronounced during certain periods, possibly due to seasonal changes, supply chain disruptions, or global market influences.

## Key Takeaways
- **Commodity-Specific Insights**: Commodities such as seafood, meat, and bananas show high sensitivity to price changes, making them candidates for more detailed analysis to help better understand price drivers.
- **Regional Disparities**: Prices in certain regions are consistently higher, highlighting the need for targeted policies or market interventions to address these discrepancies and improve food affordability.
  
## Recommendations for Future Work
- **Time Series Forecasting**: Implementing time-series forecasting models (e.g., ARIMA) could help predict future price trends and allow for better planning to mitigate price fluctuations, particularly in volatile regions.
- **Deeper Commodity-Specific Analysis**: High-priced commodities like seafood and meat should undergo further analysis to uncover supply chain inefficiencies or other factors affecting their prices.
- **Policy Recommendations**: Insights into regional disparities could guide policymakers in focusing efforts on regions where food prices are consistently higher, helping to ensure food affordability across the country.

## Tools and Resources Used
This project utilized:
- **Streamlit**: For building the interactive data exploration dashboard.
- **Pandas**: To preprocess and manipulate the dataset.
- **Plotly**: For generating interactive visualizations like bar charts, pie charts, and line graphs.
- **World Food Programme (WFP)**: The dataset was sourced from the WFP Price Database, providing an extensive view of food prices across different regions in the Philippines.

We believe the insights generated from this exploration will be useful for market analysts, policymakers, and researchers seeking to understand the dynamics of food pricing in the Philippines and plan strategic interventions accordingly.
"""
)
