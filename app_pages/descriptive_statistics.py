import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

st.header("Descriptive Statistics for Philippine Food Prices")

# Access the cached data from session_state
df = st.session_state.get("df", pd.DataFrame())

# List of default columns to display in multiselect
default_columns = ["#item+name", "#value", "#adm1+name", "#date"]

# Ensure that default columns exist in the dataframe
available_columns = df.columns.tolist()
valid_default_columns = [col for col in default_columns if col in available_columns]

# Tabs for dataset view and sales by percentiles
tab1, tab2 = st.tabs(["Dataset", "Price Percentiles & Summary"])

# Tab 1: Dataset Display
with tab1:
    with st.expander("Show Dataset"):
        # Multiselect to filter displayed columns
        selected_columns = st.multiselect(
            "Filter Columns:", available_columns, default=valid_default_columns
        )
        if selected_columns:
            st.dataframe(df[selected_columns], use_container_width=True)
        else:
            st.write("No columns selected.")

# Tab 2: Price Percentiles & Summary
with tab2:
    st.caption("Food Prices by Percentiles")

    # Ensure that the `#value` column exists before calculating percentiles
    if "#value" in df.columns:
        # Percentiles and Metrics Display
        p1, p2, p3, p4, p5 = st.columns(5)

        with p1:
            st.info("Percentile 25 %", icon="⏱")
            st.metric(label="PHP", value=f"{np.percentile(df['#value'], 25):,.2f}")

        with p2:
            st.info("Percentile 50 %", icon="⏱")
            st.metric(label="PHP", value=f"{np.percentile(df['#value'], 50):,.2f}")

        with p3:
            st.info("Percentile 75 %", icon="⏱")
            st.metric(label="PHP", value=f"{np.percentile(df['#value'], 75):,.2f}")

        with p4:
            st.info("Percentile 100 %", icon="⏱")
            st.metric(label="PHP", value=f"{np.percentile(df['#value'], 100):,.2f}")

        with p5:
            st.info("Percentile 0 %", icon="⏱")
            st.metric(label="PHP", value=f"{np.percentile(df['#value'], 0):,.2f}")

        # Display number summary for numerical data
        st.subheader("Descriptive Summary of Prices")
        st.dataframe(df["#value"].describe(), use_container_width=True)

        # Adding a box plot for price distribution
        st.subheader("Price Distribution (Box Plot)")
        fig = px.box(df, y="#value", title="Distribution of Prices in PHP")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("The `#value` column is missing from the dataset.")


# Sidebar for additional analysis
def categorical_analysis():
    st.sidebar.markdown("### Additional Analysis")
    column = st.sidebar.selectbox(
        "Select a Categorical Column", ["#adm1+name", "#item+name", "#item+type"]
    )
    analysis_type = st.sidebar.radio("Analysis Type", ["Categorical", "Numerical"])

    c1, c2 = st.columns([2, 1])

    # Categorical analysis - frequency distribution with pie chart option
    if analysis_type == "Categorical":
        with c1:
            st.subheader(f"Distribution of {column}")
            freq_dist = df[column].value_counts().reset_index()
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
            st.dataframe(df["#value"].describe(), use_container_width=True)

        with c2:
            st.subheader("Total Sales")
            total_sales = np.sum(df["#value"])
            avg_sales = np.average(df["#value"])
            st.metric(
                label="Total PHP",
                value=f"{total_sales:,.2f}",
                delta=f"{avg_sales:,.2f} Avg",
                delta_color="inverse",
            )


# Apply styles to metric cards
style_metric_cards(
    background_color="#00000000",
    border_left_color="#000000",
    border_color="#000000",
    box_shadow="#F71938",
)

# Call the function for sidebar analysis
categorical_analysis()
