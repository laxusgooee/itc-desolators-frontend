import streamlit as st
from services.nlp_api_client import nlp_api

@st.dialog("Add New Ticket for NLP Analysis")
def nlp_add_new_ticket():
    st.write("Enter the ticket text below to process it through the NLP pipeline (classification, NER, and LLM drafting).")
    
    with st.form("add_ticket_form", clear_on_submit=True):
        text = st.text_area("Ticket Text", placeholder="Describe the issue or request...", height=200)
        submit = st.form_submit_button("Process Ticket", type="primary", use_container_width=True)
        
        if submit:
            if not text.strip():
                st.error("Please enter some text.")
            else:
                with st.spinner("Processing ticket..."):
                    result = nlp_api.create_ticket(text)
                    if result:
                        st.success(f"Ticket processed successfully! (ID: {result.get('ticket_id') or 'New'})")
                        # Prepend to user_tickets so it shows at the top
                        if "user_tickets" not in st.session_state:
                            st.session_state.user_tickets = []
                        st.session_state.user_tickets.insert(0, result)
                        
                        # Select the new ticket
                        st.session_state.selected_ticket_id = result.get('ticket_id')
                        
                        # Reset pagination to show the top (where the new ticket is)
                        st.session_state.current_page = 0
                        
                        st.rerun()
                    else:
                        st.error("Failed to process ticket. Please try again.")
