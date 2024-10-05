import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import time
from numerize.numerize import numerize
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go


st.header("Food Prices Analysis, KPI, Trends & Predictions")

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('data/wfp_food_prices_phl.csv', skiprows=1)
    data['#date'] = pd.to_datetime(data['#date'])
    return data

df = load_data()

# Sidebar filters
region = st.sidebar.multiselect(
    "SELECT REGION",
    options=df["#adm1+name"].unique(),
    default=df[""].unique(),
)

commodity = st.sidebar.multiselect(
    "SELECT COMMODITY",
    options=df["#item+name"].unique(),
    default=df["#item+name"].unique(),
)

# Use isin() for filtering based on multiselect values
df_selection = df[
    (df['#adm1+name'].isin(region)) & 
    (df['#item+name'].isin(commodity))
]

# Function for Home Page
def Home():
    with st.expander("VIEW DATASET"):
        show_data = st.multiselect('Filter: ', df_selection.columns, default=["#item+name", "#value", "#adm1+name", "#date"])
        st.dataframe(df_selection[show_data], use_container_width=True)

    # Compute top analytics
    total_price = float(pd.Series(df_selection['#value']).sum())
    price_mode = float(pd.Series(df_selection['#value']).mode())
    price_mean = float(pd.Series(df_selection['#value']).mean())
    price_median = float(pd.Series(df_selection['#value']).median())

    # KPIs
    total1, total2, total3, total4 = st.columns(4, gap='small')
    with total1:
        st.info('Total Price', icon="💰")
        st.metric(label="Total PHP", value=f"{total_price:,.0f} PHP")

    with total2:
        st.info('Most Common Price', icon="💰")
        st.metric(label="Mode PHP", value=f"{price_mode:,.0f} PHP")

    with total3:
        st.info('Average Price', icon="💰")
        st.metric(label="Average PHP", value=f"{price_mean:,.0f} PHP")

    with total4:
        st.info('Median Price', icon="💰")
        st.metric(label="Median PHP", value=f"{price_median:,.0f} PHP")

    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    # Variable Distribution Histogram
    with st.expander("PRICE DISTRIBUTION"):
        df_selection['#value'].hist(figsize=(16, 8), color='#898784', rwidth=0.9)
        st.pyplot()

# Function for Graphs
def graphs():
    # Bar graph: price by commodity
    price_by_commodity = df_selection.groupby(by=["#item+name"])[["#value"]].sum().sort_values(by="#value")
    
    fig_price = px.bar(
        price_by_commodity,
        x="#value",
        y=price_by_commodity.index,
        orientation="h",
        title="<b> Price by Commodity </b>",
        color_discrete_sequence=["#0083B8"] * len(price_by_commodity),
        template="plotly_white",
    )
    fig_price.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )

    # Line graph: price trend over time
    price_by_date = df_selection.groupby(by=["#date"])[["#value"]].sum()
    
    fig_date = px.line(
        price_by_date,
        x=price_by_date.index,
        y="#value",
        title="<b> Price Trend Over Time </b>",
        color_discrete_sequence=["#0083B8"] * len(price_by_date),
        template="plotly_white",
    )
    fig_date.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_date, use_container_width=True)
    right.plotly_chart(fig_price, use_container_width=True)


# Function for Progress Bar
def Progressbar():
    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",
        unsafe_allow_html=True,
    )
    target = 1000000  # Sample target
    current = df_selection['#value'].sum()
    percent = round((current / target * 100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target reached!")
    else:
        st.write("You have", percent, "% of", f"{target:,.0f} PHP")
        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete + 1)

# Sidebar menu
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0,
        )
    if selected == "Home":
        Home()
        graphs()
    if selected == "Progress":
        Progressbar()
        graphs()

sideBar()
