import pandas as pd
import streamlit as st

from components.sidebar import render_sidebar
from services.api_client import api
from utils.formatters import format_currency

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
render_sidebar()

st.title("📊 Dashboard")

items = api.get_items()

if not items:
    st.warning("No data available yet. Create some items first.")
    st.stop()

df = pd.DataFrame(items)

# ── KPI row ────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Total Items", len(df))
col2.metric("Active Items", int(df["is_active"].sum()))
col3.metric("Avg. Price", format_currency(df["price"].mean()))

st.divider()

# ── Price distribution ──────────────────────────────────────────────────────────
st.subheader("Price Distribution")
st.bar_chart(df.set_index("name")["price"])

st.divider()

# ── Raw data ───────────────────────────────────────────────────────────────────
with st.expander("📄 Raw data"):
    st.dataframe(df, use_container_width=True, hide_index=True)
