import streamlit as st
from services.classification_api_client import classification_api
from components.sidebar import render_sidebar
from components.skeleton import render_skeleton
from components.classification_dialog import open_classification_dialog
from components.classification_result_row import render_classification_result_row
from components.classification_accuracy_badge import render_accuracy_badge
from components.classification_confusion_matrix_heatmap import render_classification_confusion_matrix_heatmap


classification_metrics = classification_api.get_metrics()
classification_class_names = [k for k in classification_metrics['classification_report'].keys() if k not in ['accuracy', 'macro avg', 'weighted avg']]


# --- Load custom CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.html(
    """
    <style>
        .st-key-image-source,
        .st-key-classification-result {
            background-color: #222831;
        }

        .st-key-image-container {
            position: relative;
            min-height: 280px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px dashed #31363F;
            /* overflow: hidden; */
        }

        .st-key-image-container-input {
            position: absolute;
            bottom: 0.5rem;
            width: calc(100% - 1rem);
            left: 0.5rem;
            right: 0.5rem;
            background-color: rgba(34, 40, 49, 0.6);
        }

        .st-key-model-metrics {
            overflow: hidden;
        }

        [data-testid="stLayoutWrapper"]:has(>.st-key-model-metrics-accuracy) {
            position: absolute;
            right: .5rem;
            width:auto;
        }

        [data-testid="stProgress"] > div[role="progressbar"] > div > div{
            background-color: #31363F;
        }
    </style>
    """
)

st.set_page_config(page_title="Classification", page_icon="📋", layout="wide")
render_sidebar()

with st.container(gap=None):
    st.html("<h2 style='margin-top:-1rem;'>Classification</h2>")
    st.caption("Upload an image to classify")

with st.container():
    col_1, col_2 = st.columns([0.5, 0.7])

    with col_1:
        with st.container(key="image-source", border=True):
            with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                st.text("IMAGE SOURCE")

                if st.button(":material/delete:", type="secondary"):
                    st.session_state.pop("uploaded_image", None)

            with st.container(key="image-container", gap=None):
                uploaded = st.session_state.get("uploaded_image")

                if uploaded is not None:
                    st.image(uploaded, width='stretch')
                else:
                    st.caption("Upload an image to classify using our AI model", text_alignment="center")

                with st.container(key="image-container-input", border=True, horizontal=True, vertical_alignment="center"):
                    with st.container(gap=None):
                        if uploaded is not None:
                            st.html(f'<h5 style="font-weight:bold;">{uploaded.name}</h5>')
                            st.caption(f"{uploaded.size // 1024} KB")
                        else:
                            st.html('<h5 style="font-weight:bold;">No file selected</h5>')
                            st.caption("JPG / PNG accepted")

                    if st.button(":material/swap_horiz:" if uploaded is not None else "Upload", type="primary"):
                        open_classification_dialog()


        st.info("""This CNN model was trained to classify plant seedlings using image features such as shape, texture, and leaf structure.""", icon="ℹ️")
    
    with col_2:
        classification_result = st.session_state.get("classification_result", None)

        if classification_result is not None:
            with st.container(key="classification-result", border=True):
                st.html(f'<h3 style="font-weight:bold;">PREDICTION RESULT </h3>')

                with st.container(gap="medium"):
                    for index, result in enumerate(classification_result["predictions"][:3]):
                        render_classification_result_row(index, result)

            with st.expander("Raw Output"):
                st.write(classification_result)
        else:
            pass
        

        with st.container(key="model-metrics", border=True):
            st.html(f'<h3 style="font-weight:bold;">Model Metrics</h3>')

            with st.container():

                st.button("Show more")

            with st.container(key="model-metrics-accuracy"):
                render_accuracy_badge(classification_metrics['classification_report']['accuracy'])

        with st.container():
            cols = st.columns(3, gap="xsmall")

            metrics = classification_metrics['classification_report']['weighted avg']

            # with cols[0]:
            #     st.metric("Accuracy", "30°F", "-9°F", border=True)

            with cols[0]:
                st.metric("Precision", f"{round(metrics["precision"] * 100)}%", border=True)

            with cols[1]:
                st.metric("Recall", f"{round(metrics["recall"] * 100)}%", border=True)
            
            with cols[2]:
                st.metric("F1 Score", f"{round(metrics["f1-score"] * 100)}%", border=True)

