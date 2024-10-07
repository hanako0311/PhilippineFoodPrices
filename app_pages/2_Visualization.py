import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

# Access the cached data from session_state
df = st.session_state["df"]

# Sidebar filters with "ALL" option
region_options = ["ALL"] + sorted(df["#adm1+name"].unique())
commodity_options = ["ALL"] + sorted(df["#item+name"].unique())

# Allow multiselect for Regions and Commodities with "ALL" option
regions_selected = st.sidebar.multiselect(
    "Select Region",
    region_options,
    default="ALL",  # Default to "ALL" option
    help="Filter report to show all regions or select multiple regions",
)

commodities_selected = st.sidebar.multiselect(
    "Select Commodity",
    commodity_options,
    default="ALL",  # Default to "ALL" option
    help="Filter report to show all commodities or select multiple commodities",
)

# Apply filters based on user selections, considering "ALL" option
if "ALL" in regions_selected:
    df_filtered = df.copy()  # If "ALL" is selected, no filtering on region
else:
    df_filtered = df[df["#adm1+name"].isin(regions_selected)]

if "ALL" in commodities_selected:
    df_filtered = df_filtered  # No filtering on commodity if "ALL" is selected
else:
    df_filtered = df_filtered[df_filtered["#item+name"].isin(commodities_selected)]

# Display key metrics using st.metric and st.info
st.markdown("## Key Metrics")
kpi1, kpi2, kpi3 = st.columns(3)

total_value = df_filtered["#value"].sum()
avg_price = df_filtered["#value"].mean()
median_price = df_filtered["#value"].median()

kpi1.info("Total Price", icon="💰")
kpi1.metric("Total PHP", f"{total_value:,.0f}")

kpi2.info("Average Price", icon="📊")
kpi2.metric("Average PHP", f"{avg_price:,.0f}")

kpi3.info("Median Price", icon="📈")
kpi3.metric("Median PHP", f"{median_price:,.0f}")


# Add a section title and description for each visualization
st.markdown("## Visualizations")

# 1. Pie Chart for Food Categories
st.markdown("### Distribution of Food Categories")
st.write(
    "This chart shows the proportion of each food category based on the selected regions and commodities."
)

category_distribution = df_filtered["#item+type"].value_counts().reset_index()
category_distribution.columns = ["Category", "Count"]

# Pie chart with sorted categories and percentage labels
pie_chart = px.pie(
    category_distribution,
    values="Count",
    names="Category",
    title="Proportion of Food Categories",
    hole=0.4,  # Donut style pie chart
)
pie_chart.update_traces(textinfo="percent+label", sort=True)
st.plotly_chart(pie_chart, use_container_width=True)

# 2. Comparison of Retail vs Wholesale Prices
st.markdown("### Retail vs Wholesale Price Comparison")
st.write(
    "This chart compares the average retail and wholesale prices for selected commodities and regions."
)

retail_vs_wholesale = (
    df_filtered.groupby(["#item+price+type", "#item+name"])["#value"]
    .mean()
    .reset_index()
)

retail_vs_wholesale_chart = px.bar(
    retail_vs_wholesale,
    x="#item+name",
    y="#value",
    color="#item+price+type",
    barmode="group",
    title="Average Retail vs Wholesale Prices by Commodity",
    labels={
        "#item+name": "Commodity",
        "#value": "Price (PHP)",
        "#item+price+type": "Price Type",
    },
)
retail_vs_wholesale_chart.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Commodity", yaxis_title="Price (PHP)"
)
st.plotly_chart(retail_vs_wholesale_chart, use_container_width=True)

# Add an additional aggregation (Top 5 and Bottom 5 commodities toggle)
st.markdown("### Commodity Price Insights")
option = st.selectbox("Select View", ["Top 5 Commodities", "Bottom 5 Commodities"])

if option == "Top 5 Commodities":
    top_commodities = (
        df_filtered.groupby("#item+name")["#value"].mean().nlargest(5).reset_index()
    )
    st.write("Top 5 Commodities by Average Price")
else:
    top_commodities = (
        df_filtered.groupby("#item+name")["#value"].mean().nsmallest(5).reset_index()
    )
    st.write("Bottom 5 Commodities by Average Price")

top_commodities_chart = px.bar(
    top_commodities,
    x="#item+name",
    y="#value",
    title=f"{option} by Average Price",
    labels={"#item+name": "Commodity", "#value": "Average Price (PHP)"},
)
st.plotly_chart(top_commodities_chart, use_container_width=True)

# 4. Price Trend Over Time (with granularity option)
st.markdown("### Price Trend Over Time")
st.write("This chart shows how prices have changed over time for the selected filters.")

granularity = st.selectbox(
    "Select Time Granularity", ["Daily", "Monthly", "Quarterly", "Yearly"]
)

# Resample data based on user-selected granularity
if granularity == "Monthly":
    df_filtered["#date"] = pd.to_datetime(df_filtered["#date"])
    price_trend = df_filtered.resample("M", on="#date")["#value"].sum().reset_index()
elif granularity == "Quarterly":
    df_filtered["#date"] = pd.to_datetime(df_filtered["#date"])
    price_trend = df_filtered.resample("Q", on="#date")["#value"].sum().reset_index()
elif granularity == "Yearly":
    df_filtered["#date"] = pd.to_datetime(df_filtered["#date"])
    price_trend = df_filtered.resample("Y", on="#date")["#value"].sum().reset_index()
else:
    price_trend = df_filtered.groupby("#date")["#value"].sum().reset_index()

price_trend_fig = px.line(
    price_trend,
    x="#date",
    y="#value",
    title=f"Price Trend Over Time ({granularity})",
    labels={"#date": "Date", "#value": "Total Price (PHP)"},
    markers=True,
)
st.plotly_chart(price_trend_fig, use_container_width=True)

# Optional: Footer Style (hide Streamlit elements)
hide_st_style = """ 
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

# Apply styles to metric cards
style_metric_cards(
    background_color="#00000000",
    border_left_color="#000000",
    border_color="#000000",
    box_shadow="#F71938",
)

st.markdown(hide_st_style, unsafe_allow_html=True)
