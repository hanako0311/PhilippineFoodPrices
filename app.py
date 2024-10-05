import streamlit as st

from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Load the TOML file directly (without any toggle)
nav = get_nav_from_toml(".streamlit/pages_sections.toml")


st.logo("logo.png")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()