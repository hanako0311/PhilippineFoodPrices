import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

st.header("Descriptive Statistics for Philippine Food Prices")

# Access the cached data from session_state
df = st.session_state.get("df", pd.DataFrame())

# Define display-friendly column names for use in the app
column_display_names = {
    "#adm1+name": "Region",
    "#adm2+name": "Subregion",
    "#loc+market+name": "Market Name",
    "#geo+lat": "Latitude",
    "#geo+lon": "Longitude",
    "#item+type": "Commodity Type",
    "#item+name": "Commodity",
    "#item+unit": "Unit",
    "#item+price+flag": "Price Flag",
    "#item+price+type": "Price Type",
    "#currency": "Currency",
    "#value": "Price (PHP)",
    "#value+usd": "Price (USD)",
}

# Create a version of the dataframe with renamed columns for display only
df_display = df.rename(columns=column_display_names)

# List of default columns to display in multiselect
default_columns = [
    "Commodity",
    "Price (PHP)",
    "Region",
    "Date",
    "Market Name",
    "Commodity Type",
    "Price Type",
]

# Ensure that default columns exist in the dataframe
available_columns = df_display.columns.tolist()
valid_default_columns = [col for col in default_columns if col in available_columns]

# Tabs for dataset view and price percentiles
tab1, tab2 = st.tabs(["Dataset", "Price Summary & Distribution"])

# Tab 1: Dataset Display
with tab1:
    with st.expander("Show Dataset"):
        # Multiselect to filter displayed columns
        selected_columns = st.multiselect(
            "Filter Columns:", available_columns, default=valid_default_columns
        )
        if selected_columns:
            st.dataframe(df_display[selected_columns], use_container_width=True)
        else:
            st.write("No columns selected.")

# Tab 2: Price Summary & Distribution
with tab2:
    st.caption("Food Prices Summary and Distribution")

    # Ensure that the 'Price (PHP)' column exists before calculating statistics
    if "Price (PHP)" in df_display.columns:
        # Percentiles and Metrics Display
        p1, p2, p3 = st.columns(3)

        with p1:
            st.info("25th Percentile", icon="⏱")
            st.metric(
                label="PHP",
                value=f"{np.percentile(df_display['Price (PHP)'], 25):,.2f}",
            )

        with p2:
            st.info("Median (50th Percentile)", icon="⏱")
            st.metric(
                label="PHP",
                value=f"{np.percentile(df_display['Price (PHP)'], 50):,.2f}",
            )

        with p3:
            st.info("75th Percentile", icon="⏱")
            st.metric(
                label="PHP",
                value=f"{np.percentile(df_display['Price (PHP)'], 75):,.2f}",
            )

        # Display descriptive summary for numerical data
        st.subheader("Descriptive Summary of Prices")
        st.write(df_display["Price (PHP)"].describe())

        # Adding a box plot for price distribution
        st.subheader("Price Distribution (Box Plot)")
        fig = px.box(df_display, y="Price (PHP)", title="Distribution of Prices in PHP")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("The 'Price (PHP)' column is missing from the dataset.")

# Sidebar for additional analysis
def categorical_analysis():
    st.sidebar.markdown("### Additional Analysis")

    # Check if the columns exist before offering them for selection
    categorical_columns = [
        "Region",
        "Subregion",
        "Market Name",
        "Commodity",
        "Commodity Type",
        "Price Type",
    ]
    valid_categorical_columns = [
        col for col in categorical_columns if col in df_display.columns
    ]

    # Selectbox based on available columns
    if valid_categorical_columns:
        column = st.sidebar.selectbox(
            "Select a Categorical Column", valid_categorical_columns
        )
        analysis_type = st.sidebar.radio("Analysis Type", ["Categorical", "Numerical"])

        c1, c2 = st.columns([2, 1])

        # Categorical analysis - frequency distribution with pie chart option
        if analysis_type == "Categorical":
            with c1:
                st.subheader(f"Distribution of {column}")
                freq_dist = df_display[column].value_counts().reset_index()
                freq_dist.columns = [column, "Count"]

                # Option to choose between Bar and Pie chart
                chart_type = st.radio(
                    "Select Chart Type", ["Bar Chart", "Pie Chart"], horizontal=True
                )

                if chart_type == "Bar Chart":
                    fig = px.bar(
                        freq_dist,
                        x=column,
                        y="Count",
                        title=f"{column} Frequency Distribution",
                    )
                else:
                    fig = px.pie(
                        freq_dist,
                        names=column,
                        values="Count",
                        title=f"{column} Distribution",
                    )

                fig.update_layout(
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                    font=dict(color="#000000"),
                )
                st.plotly_chart(fig, use_container_width=True)

        # Numerical analysis - descriptive summary
        else:
            with c1:
                st.subheader("Numerical Summary of Prices")
                st.write(df_display["Price (PHP)"].describe())

            with c2:
                st.subheader("Sum of prices")
                total_sales = np.sum(df_display["Price (PHP)"])
                avg_sales = np.average(df_display["Price (PHP)"])
                st.metric(
                    label="Total PHP",
                    value=f"{total_sales:,.2f}",
                    delta=f"{avg_sales:,.2f} Avg",
                    delta_color="inverse",
                )

    else:
        st.sidebar.error("No valid categorical columns available for analysis.")

# Apply styles to metric cards
style_metric_cards(
    background_color="#00000000",
    border_left_color="#000000",
    border_color="#000000",
    box_shadow="#F71938",
)

# Call the function for sidebar analysis
categorical_analysis()
