import streamlit as st
from utils.formatters import truncate
from config.settings import settings


def render_sidebar() -> None:
    """Render the global sidebar with navigation info and settings."""
    with st.sidebar:
        with st.container():
            st.title(f"{settings.APP_ICON} {settings.APP_NAME}")

            st.space("medium")

            with st.container(gap="small"):
                st.page_link("app.py", label="Home", icon="🏠")
                st.page_link("pages/1_classification.py", label="Classification", icon="📋")
                st.page_link("pages/2_nlp.py", label="NLP", icon="📝")

            
        with st.container():
            st.markdown("---")
            st.caption(f"`{truncate(settings.API_URL, 40)}`", width="stretch", text_alignment="center")
