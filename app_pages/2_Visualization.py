import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

# Access the cached data from session_state
df = st.session_state["df"]

# Rename columns for user-friendly display
df_display = df.rename(
    columns={
        "#adm1+name": "Region",
        "#item+name": "Commodity",
        "#value": "Price (PHP)",
        "#item+type": "Commodity Type",
        "#item+price+type": "Price Type",
        "#date": "Date",
    }
)

# Sidebar filters with "ALL" option
region_options = ["ALL"] + sorted(df_display["Region"].unique())
commodity_options = ["ALL"] + sorted(df_display["Commodity"].unique())

# Allow multiselect for Regions and Commodities with "ALL" option
regions_selected = st.sidebar.multiselect(
    "Select Region",
    region_options,
    default="ALL",
    help="Filter report to show all regions or select multiple regions",
)

commodities_selected = st.sidebar.multiselect(
    "Select Commodity",
    commodity_options,
    default="ALL",
    help="Filter report to show all commodities or select multiple commodities",
)

# Apply filters based on user selections, considering "ALL" option
df_filtered = df_display.copy()
if "ALL" not in regions_selected:
    df_filtered = df_filtered[df_filtered["Region"].isin(regions_selected)]

if "ALL" not in commodities_selected:
    df_filtered = df_filtered[df_filtered["Commodity"].isin(commodities_selected)]

# Display key metrics using st.metric and st.info
st.markdown("## Key Metrics")
kpi2, kpi3 = st.columns(2)

avg_price = df_filtered["Price (PHP)"].mean()
median_price = df_filtered["Price (PHP)"].median()

kpi2.info("Average Price", icon="\U0001F4CA")
kpi2.metric("Average PHP", f"{avg_price:,.0f}")

kpi3.info("Median Price", icon="\U0001F4C8")
kpi3.metric("Median PHP", f"{median_price:,.0f}")

# Add a section title and description for each visualization
st.markdown("## Visualizations")

# 1. Pie Chart for Commodity Distribution
st.markdown("### Distribution of Food Categories")
st.write(
    "This chart shows the proportion of each food category (e.g., grains, meats) for the selected regions and commodities. "
    "If you filter by region or commodity, the chart will adjust to show the distribution within that subset."
)

category_distribution = df_filtered["Commodity Type"].value_counts().reset_index()
category_distribution.columns = ["Category", "Count"]

# Pie chart with sorted categories and percentage labels
pie_chart = px.pie(
    category_distribution,
    values="Count",
    names="Category",
    title="Proportion of Food Categories",
    hole=0.4,
)
pie_chart.update_traces(textinfo="percent+label", sort=True)
st.plotly_chart(pie_chart, use_container_width=True)

# 2. Regional and Commodity Price Breakdown
if len(regions_selected) > 1 and len(commodities_selected) > 1:
    st.markdown("### Price Breakdown for Selected Regions and Commodities")
    price_breakdown = (
        df_filtered.groupby(["Region", "Commodity"])["Price (PHP)"].mean().reset_index()
    )

    price_breakdown_chart = px.bar(
        price_breakdown,
        x="Region",
        y="Price (PHP)",
        color="Commodity",
        barmode="group",
        title="Average Price by Region and Commodity",
        labels={
            "Region": "Region",
            "Price (PHP)": "Price (PHP)",
            "Commodity": "Commodity",
        },
    )
    st.plotly_chart(price_breakdown_chart, use_container_width=True)

# 3. Regional Price Breakdown for Selected Commodity
if len(regions_selected) > 1 and len(commodities_selected) == 1:
    st.markdown("### Regional Price Breakdown for Selected Commodity")
    regional_price_breakdown = (
        df_filtered.groupby(["Region"])["Price (PHP)"].mean().reset_index()
    )

    regional_price_chart = px.bar(
        regional_price_breakdown,
        x="Region",
        y="Price (PHP)",
        title=f"Average Price of {commodities_selected[0]} by Region",
        labels={"Region": "Region", "Price (PHP)": "Price (PHP)"},
    )
    st.plotly_chart(regional_price_chart, use_container_width=True)

# 4. Commodity Price Comparison for Selected Region
if len(regions_selected) == 1 and len(commodities_selected) > 1:
    st.markdown("### Commodity Price Comparison for Selected Region")
    commodity_price_breakdown = (
        df_filtered.groupby(["Commodity"])["Price (PHP)"].mean().reset_index()
    )

    commodity_price_chart = px.bar(
        commodity_price_breakdown,
        x="Commodity",
        y="Price (PHP)",
        title=f"Average Price of Commodities in {regions_selected[0]}",
        labels={"Commodity": "Commodity", "Price (PHP)": "Price (PHP)"},
    )
    st.plotly_chart(commodity_price_chart, use_container_width=True)

# 5. Comparison of Retail vs Wholesale Prices
st.markdown("### Retail vs Wholesale Price Comparison")
st.write(
    "This chart compares the average retail and wholesale prices for selected commodities and regions. "
    "It helps to understand how prices differ between the two markets."
)

retail_vs_wholesale = (
    df_filtered.groupby(["Price Type", "Commodity"])["Price (PHP)"].mean().reset_index()
)

retail_vs_wholesale_chart = px.bar(
    retail_vs_wholesale,
    x="Commodity",
    y="Price (PHP)",
    color="Price Type",
    barmode="group",
    title="Average Retail vs Wholesale Prices by Commodity",
    labels={
        "Commodity": "Commodity",
        "Price (PHP)": "Price (PHP)",
        "Price Type": "Price Type",
    },
)
retail_vs_wholesale_chart.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Commodity", yaxis_title="Price (PHP)"
)
st.plotly_chart(retail_vs_wholesale_chart, use_container_width=True)

# 6. Commodity Price Insights (Top 5 and Bottom 5)
st.markdown("### Commodity Price Insights")
st.write(
    "This chart shows the top 5 or bottom 5 commodities based on average price. "
    "This helps identify the most expensive and most affordable commodities in the selected regions."
)

option = st.selectbox("Select View", ["Top 5 Commodities", "Bottom 5 Commodities"])

if option == "Top 5 Commodities":
    top_commodities = (
        df_filtered.groupby("Commodity")["Price (PHP)"].mean().nlargest(5).reset_index()
    )
    st.write("Top 5 Commodities by Average Price")
else:
    top_commodities = (
        df_filtered.groupby("Commodity")["Price (PHP)"]
        .mean()
        .nsmallest(5)
        .reset_index()
    )
    st.write("Bottom 5 Commodities by Average Price")

top_commodities_chart = px.bar(
    top_commodities,
    x="Commodity",
    y="Price (PHP)",
    title=f"{option} by Average Price",
    labels={"Commodity": "Commodity", "Price (PHP)": "Average Price (PHP)"},
)
st.plotly_chart(top_commodities_chart, use_container_width=True)

# 7. Price Trend Over Time
st.markdown("### Price Trend Over Time")
st.write(
    "This chart shows how prices have changed over time based on the selected filters. "
    "The chart displays yearly trends to provide a clearer view of long-term changes."
)

# Resample data for yearly granularity
df_filtered["Date"] = pd.to_datetime(df_filtered["Date"])
price_trend = df_filtered.resample("Y", on="Date")["Price (PHP)"].mean().reset_index()

price_trend_fig = px.line(
    price_trend,
    x="Date",
    y="Price (PHP)",
    title="Price Trend Over Time (Yearly)",
    labels={"Date": "Date", "Price (PHP)": "Average Price (PHP)"},
    markers=True,
)
st.plotly_chart(price_trend_fig, use_container_width=True)

# Apply styles to metric cards
style_metric_cards(
    background_color="#00000000",
    border_left_color="#000000",
    border_color="#000000",
    box_shadow="#F71938",
)
