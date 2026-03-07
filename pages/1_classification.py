from shutil import which

import streamlit as st

from components.sidebar import render_sidebar
from components.classification_dialog import open_classification_dialog

# --- Load custom CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.html(
    """
    <style>
        .st-key-image-container {
            position: relative;
            min-height: 300px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .st-key-image-container-input {
            position: absolute;
            bottom: 0.5rem;
            width: calc(100% - 0.6rem);
            left: 0.3rem;
            right: 0.3rem;
            background-color: rgba(34, 40, 49,0.3);
        }
    </style>
    """
)

st.set_page_config(page_title="Classification", page_icon="📋", layout="wide")
render_sidebar()

with st.container(gap=None):
    st.html("<h2>Classification</h2>")
    st.caption("Upload an image to classify")

st.space('small')

with st.container():
    col_1, col_2 = st.columns([0.4, 0.8])

    with col_1:
        with st.container(border=True):
            st.text("IMAGE SOURCE")

            with st.container(key="image-container"):

                st.text("Upload an image to classify using our AI model", text_alignment="center")

                with st.container(key="image-container-input", border=True, horizontal=True, vertical_alignment="center"):
                    with st.container(gap=None):
                        st.html(f'<h5 style="font-weight:bold;">sample_retriver.jpg</h5>')
                        st.caption(f"224 x 224 pixels . RGB")

                    if st.button("Reset", type="primary"):
                        open_classification_dialog()


        st.info("""This CNN model was trained to classify plant seedlings using image features such as shape, texture, and leaf structure.""", icon="ℹ️")
    
    with col_2:
        with st.container(border=True):
            st.html(f'<h3 style="font-weight:bold;">Some Title</h3>')

        st.space()

        with st.container(border=True):
            st.html(f'<h3 style="font-weight:bold;">Some Title</h3>')

        st.space()

        with st.container():
            cols = st.columns(3, gap="large")

            with cols[0]:
                with st.container(border=True):
                    st.html(f'<h4 style="font-weight:semi-bold;">Some metric</h4>')

            with cols[1]:
                with st.container(border=True):
                    st.html(f'<h4 style="font-weight:semi-bold;">Some metric</h4>')

            with cols[2]:
                with st.container(border=True):
                    st.html(f'<h4 style="font-weight:semi-bold;">Some Metric</h4>')

