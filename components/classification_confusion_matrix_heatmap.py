import streamlit as st
import pandas as pd
import altair as alt

def render_classification_confusion_matrix_heatmap(confusion_matrix: list[list[int]], class_names: list[str]) -> None:
    """Render a confusion matrix as a heatmap using Altair.
    
    Parameters
    ----------
    confusion_matrix : list[list[int]]
        The 2D confusion matrix.
    class_names : list[str]
        The list of class names for labels.
    """
    # Transform to tidy format for Altair
    data = []
    for i, row in enumerate(confusion_matrix):
        actual = class_names[i]
        for j, val in enumerate(row):
            predicted = class_names[j]
            data.append({
                "Actual": actual,
                "Predicted": predicted,
                "Count": val
            })
    
    df = pd.DataFrame(data)
    
    # Create Altair Heatmap
    base = alt.Chart(df).encode(
        x=alt.X('Predicted:N', title=None, sort=class_names, axis=None),
        y=alt.Y('Actual:N', title=None, sort=class_names, axis=None)
    ).properties(
        width='container',
        height=400
    )
    
    # Heatmap rectangles
    heatmap = base.mark_rect().encode(
        color=alt.Color('Count:Q', scale=alt.Scale(scheme='blues'), title='Count'),
        tooltip=['Actual', 'Predicted', 'Count']
    )
    
    # Text labels in cells
    text = base.mark_text(baseline='middle').encode(
        text='Count:Q',
        color=alt.condition(
            alt.datum.Count > df['Count'].max() / 2,
            alt.value('white'),
            alt.value('black')
        )
    )
    
    chart = (heatmap + text).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(chart, width='stretch')
