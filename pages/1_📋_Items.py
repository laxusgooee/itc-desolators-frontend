import streamlit as st

from components.sidebar import render_sidebar
from services.api_client import api
from utils.formatters import bool_to_badge, format_currency, truncate

st.set_page_config(page_title="Items", page_icon="📋", layout="wide")
render_sidebar()

st.title("📋 Items")
st.markdown("Manage your items below.")

# ── Fetch & display ────────────────────────────────────────────────────────────
items = api.get_items()

if items:
    # Build display-friendly table data
    rows = [
        {
            "ID": item["id"],
            "Name": item["name"],
            "Description": truncate(item.get("description") or "—"),
            "Price": format_currency(item["price"]),
            "Status": bool_to_badge(item.get("is_active", True)),
        }
        for item in items
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("No items found. Create one below!")

st.divider()

# ── Create ─────────────────────────────────────────────────────────────────────
with st.expander("➕ Create new item", expanded=not items):
    with st.form("create_item_form", clear_on_submit=True):
        name = st.text_input("Name *")
        description = st.text_area("Description")
        price = st.number_input("Price *", min_value=0.0, step=0.01, format="%.2f")
        submitted = st.form_submit_button("Create", type="primary")

    if submitted:
        if not name or price <= 0:
            st.warning("Name and a positive price are required.")
        else:
            result = api.create_item({"name": name, "description": description, "price": price})
            if result:
                st.success(f"✅ Item **{result['name']}** created!")
                st.rerun()

# ── Delete ─────────────────────────────────────────────────────────────────────
if items:
    st.divider()
    with st.expander("🗑️ Delete an item"):
        item_ids = [item["id"] for item in items]
        del_id = st.selectbox("Select item ID to delete", item_ids)
        if st.button("Delete", type="secondary"):
            if api.delete_item(del_id):
                st.success(f"Deleted item {del_id}.")
                st.rerun()
