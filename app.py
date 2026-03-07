import streamlit as st

from components.sidebar import render_sidebar
from config.settings import settings

# --- Page config (must be the first Streamlit call) ---
st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon=settings.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load custom CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Sidebar ---
render_sidebar()

# --- Home page content ---
st.title(f"{settings.APP_ICON} {settings.APP_NAME}")
st.markdown(
    """
    Welcome! Use the sidebar to navigate between pages.

    | Page | Description |
    |------|-------------|
    | 📋 Items | Browse, create, update and delete items |
    | 📊 Dashboard | Visual summary of your data |
    """
)
