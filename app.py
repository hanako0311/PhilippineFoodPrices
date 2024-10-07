import pandas as pd
import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide", initial_sidebar_state="expanded")


# Load data with caching in app.py
@st.cache_data
def load_data():
    # Adjust based on your dataset structure
    data = pd.read_csv("data/wfp_food_prices_phl.csv", skiprows=1)
    data["#date"] = pd.to_datetime(data["#date"])
    return data


# Load the data once and store it in session state
if "df" not in st.session_state:
    st.session_state["df"] = load_data()

# Load the TOML file directly for navigation
nav = get_nav_from_toml(".streamlit/pages_sections.toml")

# Display logo and navigation
st.logo("logo.png")
pg = st.navigation(nav)
add_page_title(pg)
pg.run()
