import streamlit as st

# Conclusion page content
st.markdown(
    """
## Summary of Insights
This analysis of **Philippine Food Prices** from 2000 to 2024 has revealed important trends and patterns regarding food price fluctuations across different regions and commodities. The interactive dashboard has allowed us to explore the following key findings:

- **Skewed Price Distribution**: The dataset shows a dominance of lower-cost items, while higher-priced commodities like seafood and meat appear as outliers.
- **Significant Regional Price Variations**: Prices vary widely between regions, with some regions reporting consistently higher prices. Factors such as infrastructure, transportation costs, and market access likely play a role in these disparities.
- **Global Market Influence**: The high correlation between **PHP** and **USD** prices (0.99) highlights the impact of global market trends on local food pricing.

## Key Takeaways
From the data, we observe:
- **Commodity-Specific Insights**: Certain commodities, especially higher-cost items like seafood and meat, demonstrate price sensitivity and could benefit from further analysis.
- **Regional Disparities**: Understanding the regional variations in prices can help policymakers focus on areas where food affordability is most at risk.
  
## Recommendations for Future Work
- **Time Series Forecasting**: To predict future trends in food prices, applying time series forecasting models (e.g., ARIMA) could provide actionable insights for planning and mitigating price volatility.
- **Further Commodity Analysis**: Conducting deeper analysis on specific high-priced commodities such as seafood and meat could assist in crafting better supply chain and pricing strategies.
- **Policy Development**: Policymakers could leverage this data to craft targeted strategies aimed at alleviating food price inflation, especially in regions with the highest costs.

## Tools and Resources Used
This project was made possible by leveraging the following tools and resources:
- **Streamlit**: To build the interactive data exploration dashboard.
- **Pandas**: For data processing and manipulation.
- **Plotly**: For creating dynamic visualizations such as pie charts, bar graphs, and line charts.
- **World Food Programme (WFP)**: The primary dataset was sourced from the WFP Price Database, offering a detailed view of food prices in the Philippines.
- **Streamlit Extras**: For enhancing the user interface with metric cards and other visual elements.

We hope the insights and findings from this exploration can be useful for researchers, policymakers, and supply chain professionals looking to understand food price dynamics in the Philippines and plan accordingly.
"""
)
