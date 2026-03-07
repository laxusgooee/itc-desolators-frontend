import time

import streamlit as st

def _animate_progress(score: float) -> None:
    bar = st.progress(0)
    for pct in range(round(score * 100)):
        time.sleep(0.01)
        bar.progress(pct + 1)


def render_classification_result_row(index: int, result: dict) -> None:
    """Render a single prediction row: rank badge, class name, confidence % and animated progress bar.

    Parameters
    ----------
    index:  0-based position in the predictions list
    result: dict with keys ``class_name`` and ``confidence`` (0–1 float)
    """
    with st.container(gap=None):
        with st.container(horizontal=True, horizontal_alignment="distribute"):
            badge_style = (
                "border:1px solid #4caf50;border-radius:8px;padding:2px 8px;color:#4caf50;"
                if index == 0
                else "border:1px solid #222831;border-radius:8px;padding:2px 8px;"
            )
            st.html(
                f"""
                <div style="display:flex;gap:.6rem;align-items:center;">
                    <div style="{badge_style}">Rank <span>#{index + 1}</span></div>
                    <h3>{result['class_name']}</h3>
                </div>
                """
            )
            st.text(f"{round(result['confidence'] * 100)}%", text_alignment="right")

        st.space("xxsmall")
        _animate_progress(result["confidence"])
