import streamlit as st
from components.classification_confusion_matrix_heatmap import render_classification_confusion_matrix_heatmap

@st.dialog("Confusion Matrix Heatmap", width="large")
def open_confusion_matrix_dialog(confusion_matrix: list[list[int]], class_names: list[str]) -> None:
    """Open a dialog showing the confusion matrix heatmap.
    
    Parameters
    ----------
    confusion_matrix : list[list[int]]
        The 2D confusion matrix.
    class_names : list[str]
        The list of class names for labels.
    """
    st.write("This heatmap shows the model's performance on the test set. Rows represent the actual class, and columns represent the predicted class.")
    
    render_classification_confusion_matrix_heatmap(confusion_matrix, class_names)
    
    if st.button("Close"):
        st.rerun()
