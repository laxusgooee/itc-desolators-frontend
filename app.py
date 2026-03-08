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
st.html(
    """
    <div style="background-color: #222831; padding: 2.5rem; border-radius: 12px; border: 1px solid #31363F; margin-bottom: 2rem;">
        <h2 style="font-weight: bold; margin-bottom: 1rem;">Project Overview: Text & Image Intelligence</h2>
        <p style="color: #EEEEEE; line-height: 1.6;">
            This project evaluates the ability to build end-to-end intelligence workflows. 
            It is divided into two core components: <b>Image Classification</b> for plant seedling identification 
            and <b>NLP Ticket Intelligence</b> for automated customer support triage and entity extraction.
        </p>
    </div>
    """
)

col1, col2 = st.columns(2, gap="medium")

with col1:
    with st.container(border=True):
        st.subheader("📋 Classification")
        st.write("Deep learning model trained to classify various species of plant seedlings from images.")
        if st.button("Open Classification", type="secondary", use_container_width=True):
            st.switch_page("pages/1_classification.py")

with col2:
    with st.container(border=True):
        st.subheader("🧠 NLP Intelligence")
        st.write("NLP workflow for ticket classification, entity extraction (Order IDs, Emails), and response drafting.")
        if st.button("Open NLP Workflow", type="secondary", use_container_width=True):
            st.switch_page("pages/2_nlp.py")
