import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from services.nlp_api_client import nlp_api
from components.nlp_add_new_ticket import nlp_add_new_ticket

st.set_page_config(
    page_title="NLP Intelligence Dashboard",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load custom CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.html(
    """
    <style>
        .st-key-tickets-container {
            position: relative;
            padding: 0px 1rem 5rem 0;
            border-right: 1px solid #f8fafc;
        }
        .st-key-tickets-list {
        
        }
        .st-key-original-text {
            background-color: #222831;
            padding: 1rem;
            border-radius: 8px;
        }
        .st-key-original-text-labels [data-testid="stElementContainer"] {
            flex-grow: 0;
        }

        .st-key-ai-text {
            margin-top: -1.8rem;
        }
        
        .selected-ticket {
            border: 2px solid #3b82f6 !important;
        }
        
        div.stButton > button {
            width: 100%;
            text-align: left;
            border: 1px solid #31333F;
            padding: 10px;
            border-radius: 8px;
            background-color: transparent;
            color: inherit;
            display: block;
            margin-bottom: 10px;
        }
        
        div.stButton > button:hover {
            border-color: #3b82f6;
        }
    </style>
    """
)

render_sidebar()

# --- Page Title ---
st.html("<h2 style='margin-top:-1rem;'>NLP Intelligence Workflow</h2>")
st.caption("Monitoring ticket classification, entity extraction, and LLM drafting performance.")

# --- Constants ---
ITEMS_PER_PAGE = 5

# --- Session State for Selection and Pagination ---
if "selected_ticket_id" not in st.session_state:
    st.session_state.selected_ticket_id = None
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "last_search" not in st.session_state:
    st.session_state.last_search = ""
if "user_tickets" not in st.session_state:
    st.session_state.user_tickets = []

# --- Fetch Tickets ---
api_tickets = nlp_api.get_ner_annotations()
# Prepend user created tickets
tickets = st.session_state.user_tickets + api_tickets

if not st.session_state.selected_ticket_id and tickets:
    st.session_state.selected_ticket_id = tickets[0]['ticket_id']

btn_col1, btn_col2 = st.columns([0.8, 0.2])
with btn_col2:
    if st.button("➕ Add New Ticket", type="secondary", use_container_width=True):
        nlp_add_new_ticket()

col_1, col_2 = st.columns([0.4, 0.6])

with col_1:
    with st.container(key="tickets-container"):
        
        search_query = st.text_input("Search ticket", placeholder="Search by ID or text...", label_visibility="hidden")
        
        # Reset pagination if search changes
        if search_query != st.session_state.last_search:
            st.session_state.current_page = 0
            st.session_state.last_search = search_query

        if tickets:
            filtered_tickets = [
                t for t in tickets 
                if search_query.lower() in t['ticket_id'].lower() or search_query.lower() in t['text'].lower()
            ]
        else:
            filtered_tickets = []

        total_pages = (len(filtered_tickets) - 1) // ITEMS_PER_PAGE + 1 if filtered_tickets else 1
        
        # Ensure current_page is within bounds
        st.session_state.current_page = min(st.session_state.current_page, total_pages - 1)
        st.session_state.current_page = max(0, st.session_state.current_page)

        # Slice tickets for the current page
        start_idx = st.session_state.current_page * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_tickets = filtered_tickets[start_idx:end_idx]

        with st.container(key="tickets-list"):
            if not tickets:
                st.info("No tickets found.")
            elif not filtered_tickets:
                st.info("No matches found.")
            else:
                for ticket in page_tickets:
                    is_selected = ticket['ticket_id'] == st.session_state.selected_ticket_id
                    
                    # We use a button to handle selection
                    # Label includes ID and some truncated text
                    label = f"**{ticket['ticket_id']}**\n\n{ticket['text'][:80]}..."
                    if st.button(label, key=f"btn_{ticket['ticket_id']}", use_container_width=True):
                        st.session_state.selected_ticket_id = ticket['ticket_id']
                        st.rerun()

                st.divider()
                
                with st.container(horizontal=True, vertical_alignment="center"):
                    st.caption(f"Page {st.session_state.current_page + 1} of {total_pages}")
                    # Pagination Buttons
                    if total_pages > 1:
                        pad_col_1, prev_col, next_col, pad_col_2 = st.columns([0.2, 0.3, 0.3, 0.2])
                        with prev_col:
                            if st.button("←", disabled=st.session_state.current_page == 0):
                                st.session_state.current_page -= 1
                                st.rerun()
                        with next_col:
                            if st.button("→", disabled=st.session_state.current_page >= total_pages - 1):
                                st.session_state.current_page += 1
                                st.rerun()
                        

if "drafts" not in st.session_state:
    st.session_state.drafts = {}

with col_2:
    if st.session_state.selected_ticket_id:
        # 1. First check if it's a locally created ticket (to avoid extra API call & 404)
        local_match = next((t for t in st.session_state.user_tickets if t['ticket_id'] == st.session_state.selected_ticket_id), None)
        
        if local_match:
            ticket_detail = local_match
        else:
            with st.spinner("Loading ticket details..."):
                ticket_detail = nlp_api.get_ticket_result(st.session_state.selected_ticket_id)
        
        if ticket_detail:
            # Fetch draft if not already in session state
            if st.session_state.selected_ticket_id not in st.session_state.drafts:
                with st.spinner("Generating AI draft..."):
                    draft = nlp_api.get_draft(
                        text=ticket_detail['text'],
                        category=ticket_detail['category'],
                        entities=ticket_detail.get('entities', [])
                    )
                    st.session_state.drafts[st.session_state.selected_ticket_id] = draft

            current_draft = st.session_state.drafts.get(st.session_state.selected_ticket_id, "")

            with st.container(border=True, key="text-container"):
                st.html("""<div style="display:flex; align-items:center; gap:2px;"><h4>Original Text</h4></div>""")

                with st.container(key="original-text"):
                    st.text(ticket_detail['text'])

                # Display Entities as highlighted chips or just a list
                if ticket_detail.get('entities'):
                    st.html("<div style='margin-top: 1rem;'><b>Detected Entities:</b></div>")
                    cols = st.columns(len(ticket_detail['entities']) + 1)
                    for i, entity in enumerate(ticket_detail['entities']):
                        with cols[i]:
                            st.html(f"""
                                <div style="display: flex;align-items: center;justify-content: center;gap: 5px; background: #222831; padding: 4px 8px; border-radius: 4px; margin-bottom: 5px;">
                                    <div class="dot" style="background-color: #3b82f6; width: 8px; height: 8px; border-radius: 50%;"> </div>
                                    <h6 style="margin: 0;">{entity['label']}: {entity['text']}</h6>
                                </div>
                            """)
                
                if ticket_detail.get('category'):
                     st.caption(f"Category: {ticket_detail['category']}")

            with st.container(border=True):
                st.html("""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0;">AI Draft response</h4>
                        <div style="padding: 2px 12px; border: 1px solid #222831; border-radius: 8px; background-color: #222831; color: #EEEEEE; font-size: 0.85rem; font-weight: 600;">GROQ</div>
                    </div>
                """)

                with st.container(key="ai-text"):
                    # Use a text area so user can edit if needed
                    st.text_area("Draft Response", value=current_draft, height=300, label_visibility="hidden", key=f"draft_{st.session_state.selected_ticket_id}")

                with st.container():
                    st.button("Send Response", type="primary")
        else:
            st.error(f"Could not load details for {st.session_state.selected_ticket_id}")
    else:
        st.info("Select a ticket to see details")
