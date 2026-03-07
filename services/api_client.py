import httpx
import streamlit as st

from config.settings import settings


class APIClient:
    """
    Thin wrapper around httpx for talking to the FastAPI backend.
    All methods raise on non-2xx and surface errors via st.error().
    """

    def __init__(self, base_url: str = settings.API_BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")

    # ------------------------------------------------------------------
    # Items
    # ------------------------------------------------------------------

    @st.cache_data(ttl=30, show_spinner=False)
    def get_items(_self) -> list[dict]:
        """Fetch all items (cached for 30 s)."""
        try:
            r = httpx.get(f"{_self.base_url}/items/")
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as exc:
            st.error(f"Failed to fetch items: {exc}")
            return []

    def get_item(self, item_id: int) -> dict | None:
        try:
            r = httpx.get(f"{self.base_url}/items/{item_id}")
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError:
            return None
        except httpx.HTTPError as exc:
            st.error(f"Error: {exc}")
            return None

    def create_item(self, payload: dict) -> dict | None:
        try:
            r = httpx.post(f"{self.base_url}/items/", json=payload)
            r.raise_for_status()
            st.cache_data.clear()
            return r.json()
        except httpx.HTTPError as exc:
            st.error(f"Failed to create item: {exc}")
            return None

    def update_item(self, item_id: int, payload: dict) -> dict | None:
        try:
            r = httpx.put(f"{self.base_url}/items/{item_id}", json=payload)
            r.raise_for_status()
            st.cache_data.clear()
            return r.json()
        except httpx.HTTPError as exc:
            st.error(f"Failed to update item: {exc}")
            return None

    def delete_item(self, item_id: int) -> bool:
        try:
            r = httpx.delete(f"{self.base_url}/items/{item_id}")
            r.raise_for_status()
            st.cache_data.clear()
            return True
        except httpx.HTTPError as exc:
            st.error(f"Failed to delete item: {exc}")
            return False


# Singleton client
api = APIClient()
