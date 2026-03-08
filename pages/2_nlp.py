import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="NLP",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load custom CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.html(
    """
    <style>
        
    </style>
    """
)

render_sidebar()

with st.container(gap=None):
    st.html("<h2 style='margin-top:-1rem;'>NLP</h2>")
    st.caption("lorem ipsum dolor sit amet consectetur adipiscing elit")