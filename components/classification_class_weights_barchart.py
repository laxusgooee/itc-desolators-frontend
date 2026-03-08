import streamlit as st
import pandas as pd
import altair as alt

def render_classification_class_weights_barchart(class_weights: dict, class_names: list[str]) -> None:
    """Render a bar chart of class weights using Altair.
    
    Parameters
    ----------
    class_weights : dict
        A dictionary mapping class indices (as strings or ints) to weights.
    class_names : list[str]
        A list of class names corresponding to the indices.
    """
    # Map weights to class names
    data = []
    for idx_str, weight in class_weights.items():
        idx = int(idx_str)
        if idx < len(class_names):
            data.append({
                "Class": class_names[idx],
                "Weight": weight
            })
    
    df = pd.DataFrame(data)
    
    # Sort by class name or weight? usually weight is interesting
    df = df.sort_values("Weight", ascending=False)
    
    # Create Altair Bar Chart
    chart = alt.Chart(df).mark_bar(
        cornerRadiusTopRight=4,
        cornerRadiusBottomRight=4,
        color="#00ADB5"  # A vibrant teal color matching a premium feel
    ).encode(
        x=alt.X('Weight:Q', title='Loss Multiplier (Weight)'),
        y=alt.Y('Class:N', title=None, sort='-x'),
        tooltip=['Class', alt.Tooltip('Weight:Q', format='.4f')]
    ).properties(
        width='container',
        height=300,
        title="Class Penalty Weights"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
        grid=False
    ).configure_view(
        strokeWidth=0
    ).configure_title(
        fontSize=16,
        anchor='start',
        color='#EEEEEE'
    )
    
    st.altair_chart(chart, use_container_width=True)
