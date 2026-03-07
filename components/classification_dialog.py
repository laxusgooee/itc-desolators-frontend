import streamlit as st

@st.dialog("Upload file")
def open_classification_dialog():
    with st.container(border=True, horizontal_alignment="center", vertical_alignment="center", height=200):
        st.text("Drag yoyr files here or browse")
        st.text("Max file size up to 500MB")

    if st.button("Upload", type="primary", width="stretch"):
        st.rerun()