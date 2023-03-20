import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import base64

BASE_URL = "https://safefiles.defiyield.info/safe/files/audit/pdf/"
SAVED_AUDITS_FILE = "../saved_audits.json"
RESULTS_PER_PAGE = 10


@st.cache_data
def scrape_audit_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    audit_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href.endswith(".pdf"):
            audit_links.append({"title": href, "url": f"{BASE_URL}{href}"})

    return audit_links





def search_audit_links(audit_links, query):
    query_tokens = set(query.lower().split())
    matching_links = []

    for link in audit_links:
        title_tokens = set(link["title"].lower().split("_"))
        if query_tokens.intersection(title_tokens):
            matching_links.append(link)

    return matching_links



def load_saved_audits():
    try:
        with open(SAVED_AUDITS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_saved_audits(saved_audits):
    with open(SAVED_AUDITS_FILE, "w") as f:
        json.dump(saved_audits, f)


def show_pdf(url):
    response = requests.get(url)
    base64_pdf = base64.b64encode(response.content).decode('utf-8')
    pdf_display = f'<div style="text-align: center;"><iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf" style="margin:auto;"></iframe></div>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def remove_pdf():
    st.markdown("", unsafe_allow_html=True)

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

        # Pagination for search results
        total_pages = (len(search_results) - 1) // RESULTS_PER_PAGE + 1
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
        start_index = (page - 1) * RESULTS_PER_PAGE
        end_index = min(start_index + RESULTS_PER_PAGE, len(search_results))

        for result in search_results[start_index:end_index]:
            st.write(f"{result['title']}")
            col2, col3, col4 = st.columns([1, 1, 1])
            with col2:
                if st.button(f"Open PDF", key=f"open_{result['title']}"):
                    show_pdf(result['url'])
            with col3:
                if st.button(f"Close PDF", key=f"close_{result['title']}"):
                    remove_pdf()
            with col4:
                if st.button(f"Save to sidebar", key=f"save_{result['title']}"):
                    st.session_state.saved_audits.append(result)
                    save_saved_audits(st.session_state.saved_audits)



    else:
        st.write(f"No audits found matching '{query}'.")

# Display saved audits in the sidebar
if st.session_state.saved_audits:
    # Pagination for saved audits
    total_saved_pages = (len(st.session_state.saved_audits) - 1) // RESULTS_PER_PAGE + 1
    saved_page = st.sidebar.number_input("Page", min_value=1, max_value=total_saved_pages, value=1, step=1)
    start_saved_index = (saved_page - 1) * RESULTS_PER_PAGE
    end_saved_index = min(start_saved_index + RESULTS_PER_PAGE, len(st.session_state.saved_audits))

    for index in range(start_saved_index, end_saved_index):
        saved_audit = st.session_state.saved_audits[index]
        with st.sidebar.container():
            col1, col2, col3 = st.sidebar.columns([1,1, 1])
            st.write(f"{saved_audit['title']}")  # Remove link from title
            with col1:
                if st.button(f"Open PDF", key=f"saved_open_{saved_audit['title']}"):
                    show_pdf(saved_audit['url'])
            with col2:
                if st.button(f"Close PDF", key=f"close_open_{saved_audit['title']}"):
                    remove_pdf()
            with col3:
                remove_button = st.button("Remove", key=f"remove_{saved_audit['title']}")

        if remove_button:
            del st.session_state.saved_audits[index]
            save_saved_audits(st.session_state.saved_audits)
            saved_audits_list.empty()
