import httpx
import streamlit as st
from typing import List, Dict, Any
from config.settings import settings

class NLPApiClient:
    """
    Client for interacting with the NLP API endpoints.
    Follows the same pattern as ClassificationAPIClient.
    """

    def __init__(self, base_url: str = settings.API_URL) -> None:
        self.base_url = base_url.rstrip("/")

    @st.cache_data(ttl=60, show_spinner=False)
    def get_labels(_self) -> List[Dict[str, Any]]:
        try:
            r = httpx.get(f"{_self.base_url}/nlp/labels", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            st.error(f"Failed to fetch NLP labels: {exc}")
            return []

    @st.cache_data(ttl=60, show_spinner=False)
    def get_ner_annotations(_self) -> List[Dict[str, Any]]:
        try:
            r = httpx.get(f"{_self.base_url}/nlp/ner-annotations", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            st.error(f"Failed to fetch NER annotations: {exc}")
            return []

    @st.cache_data(ttl=60, show_spinner=False)
    def get_metrics(_self) -> Dict[str, Any]:
        try:
            r = httpx.get(f"{_self.base_url}/nlp/metrics", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            st.error(f"Failed to fetch NLP metrics: {exc}")
            return {}

    @st.cache_data(ttl=30, show_spinner=False)
    def get_results(_self) -> List[Dict[str, Any]]:
        try:
            r = httpx.get(f"{_self.base_url}/nlp/results", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            st.error(f"Failed to fetch NLP results: {exc}")
            return []

    def get_ticket_result(self, ticket_id: str) -> Dict[str, Any] | None:
        try:
            r = httpx.get(f"{self.base_url}/nlp/{ticket_id}", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            st.error(f"Failed to fetch result for ticket {ticket_id}: {exc}")
            return None

    def create_ticket(self, text: str) -> Dict[str, Any] | None:
        try:
            r = httpx.post(f"{self.base_url}/nlp/", json={"text": text}, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            st.error(f"Failed to create ticket: {exc}")
            return None

    def get_draft(self, text: str, category: str, entities: List[Dict[str, Any]]) -> str:
        try:
            payload = {
                "text": text,
                "category": category,
                "entities": entities
            }
            r = httpx.post(f"{self.base_url}/nlp/draft", json=payload, timeout=15)
            r.raise_for_status()
            return r.json().get("draft_response", "")
        except Exception as exc:
            st.error(f"Failed to generate draft: {exc}")
            return ""

# Singleton instance
nlp_api = NLPApiClient()

