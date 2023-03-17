import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://safefiles.defiyield.info/safe/files/audit/pdf/"
SAVED_AUDITS_FILE = "saved_audits.json"

@st.cache_data
def scrape_audit_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    audit_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href.endswith(".pdf"):
            audit_links.append({"title": href, "url": f"{BASE_URL}/{href}"})

    return audit_links

def search_audit_links(audit_links, query):
    return [link for link in audit_links if query.lower() in link["title"].lower()]

def load_saved_audits():
    try:
        with open(SAVED_AUDITS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_saved_audits(saved_audits):
    with open(SAVED_AUDITS_FILE, "w") as f:
        json.dump(saved_audits, f)

st.title("Blockchain Security Audit Search")
st.write("Search for security audits hosted on https://safefiles.defiyield.info/safe/files/audit/pdf/")

query = st.text_input("search:")

saved_audits = st.sidebar.title("Saved Audits")
saved_audits_list = st.sidebar.empty()

# Load saved audits from file
if "saved_audits" not in st.session_state:
    st.session_state.saved_audits = load_saved_audits()

if query:
    audit_links = scrape_audit_links()
    search_results = search_audit_links(audit_links, query)

    if search_results:
        st.write(f"Found {len(search_results)} audit(s) matching '{query}':")
        for result in search_results:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"[{result['title']}]({result['url']})")
            with col2:
                save_button = st.button(f"Save", key=result['title'])

            # Save the audit if the save button is clicked
            if save_button:
                st.session_state.saved_audits.append(result)
                save_saved_audits(st.session_state.saved_audits)
                saved_audits_list.write(f"[{result['title']}]({result['url']})")

    else:
        st.write(f"No audits found matching '{query}'.")

# Display saved audits in the sidebar
if st.session_state.saved_audits:
    for index, saved_audit in enumerate(st.session_state.saved_audits):
        with st.sidebar.container():
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                st.write(f"[{saved_audit['title']}]({saved_audit['url']})")
            with col2:
                remove_button = st.button("Remove", key=f"remove_{saved_audit['title']}")

            if remove_button:
                del st.session_state.saved_audits[index]
                save_saved_audits(st.session_state.saved_audits)
                saved_audits_list.empty()

