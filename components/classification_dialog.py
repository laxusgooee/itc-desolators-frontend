import streamlit as st
from services.classification_api_client import classification_api

@st.dialog("Upload file")
def open_classification_dialog():
    st.html(
        """
        <style>
            .st-key-image-upload-container {
                background-color: #222831;
            }
        </style>
        """
    )

    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if st.button("Upload", type="primary", width="stretch", disabled=uploaded_file is None):
        with st.spinner("Classifying…"):
            result = classification_api.classify(uploaded_file)
            if result is not None:
                st.session_state["uploaded_image"] = uploaded_file
                st.session_state["classification_result"] = result
                st.rerun()