import streamlit as st


_SKELETON_CSS = """
<style>
@keyframes skeleton-shimmer {
    0%   { background-position: -600px 0; }
    100% { background-position:  600px 0; }
}

.skeleton-block {
    border-radius: 6px;
    background: linear-gradient(
        90deg,
        #2a2f3a 25%,
        #353b48 50%,
        #2a2f3a 75%
    );
    background-size: 600px 100%;
    animation: skeleton-shimmer 1.4s infinite linear;
}

.skeleton-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
    padding: 4px 0;
}
</style>
"""


def render_skeleton(rows: int = 3, height: int = 18) -> None:
    """Render an animated shimmer skeleton placeholder.

    Parameters
    ----------
    rows:   number of skeleton lines to show (default 3)
    height: height of each row in pixels (default 18)
    """
    rows_html = ""
    for i in range(rows):
        width = "60" if i == rows - 1 else "100"
        rows_html += f'<div class="skeleton-block" style="height:{height}px; width:{width}%;"></div>\n'

    st.html(f"""
{_SKELETON_CSS}
<div class="skeleton-wrap">
{rows_html}
</div>
""")
