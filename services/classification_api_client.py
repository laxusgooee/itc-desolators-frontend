import httpx
import streamlit as st

from config.settings import settings


class ClassificationAPIClient:
    """
    Thin wrapper around httpx for talking to the FastAPI backend.
    All methods raise on non-2xx and surface errors via st.error().
    """

    def __init__(self, base_url: str = settings.API_URL) -> None:
        self.base_url = base_url.rstrip("/")

    
    def classify(self, file: bytes) -> dict | None:
        try:
            r = httpx.post(f"{self.base_url}/classification/classify", files={"file": (file.name, file.getvalue(), file.type)})
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as exc:
            st.error(f"Failed to classify: {exc}")
            return None

    @st.cache_data(ttl=30, show_spinner=False)
    def get_metrics(_self) -> dict | None:
        try:
            r = httpx.get(f"{_self.base_url}/classification/metrics")
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as exc:
            st.error(f"Failed to get metrics: {exc}")
            return None


# Singleton client
classification_api = ClassificationAPIClient()
