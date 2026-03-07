import streamlit as st

def render_accuracy_badge(score: float) -> None:
    """Render a styled accuracy badge based on the provided score.
    
    Parameters
    ----------
    score : float
        A value between 0 and 1 representing the accuracy.
    """
    percentage = round(score * 100)
    
    # Determine colors based on score
    if score >= 0.8:
        # Success Green
        border_color = "#4caf50"
        bg_color = "#e8f5e9"
        text_color = "#2e7d32"
    elif score >= 0.5:
        # Warning Orange
        border_color = "#ff9800"
        bg_color = "#fff3e0"
        text_color = "#ef6c00"
    else:
        # Error Red
        border_color = "#f44336"
        bg_color = "#ffebee"
        text_color = "#c62828"
    
    badge_html = f"""
   <div style="height:120px; overflow:hidden;">
    <div style="
        display: flex;
        align-items: start;
        justify-content: center;
        border: 8px solid {border_color};
        border-radius: 50%;
        font-weight: bold;
        font-size: 1.1rem;
        text-align: center;
        width: 180px;
        height: 180px
    ">
        <div style="padding-top: 5px;">
            <span style="font-size: 12px;">Accuracy</span>
        <h2>{percentage}%</h2>
        </div>
    </div>
   </div>
    """
    
    st.html(badge_html)
