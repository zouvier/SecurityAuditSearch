# Blockchain Security Audit's Search

A Streamlit app to search for security audits hosted on [https://safefiles.defiyield.info/safe/files/audit/pdf/](https://safefiles.defiyield.info/safe/files/audit/pdf/). Users can search for audits, save them to a list, and remove them from the list. The saved audits will persist across page refreshes and even after closing and reopening the browser tab.

## Features

- Search for security audits for blockchain projects by entering a search term
- Display the search results with links to the audit files
- Save audits to a list in the sidebar
- Remove audits from the saved list
- Persist the saved audits using a JSON file

## Installation

1. Install latest python version
2. Clone the repo: `git clone https://github.com/your_username/blockchain_audit_search.git`
3. Change to the project directory: `cd blockchain_audit_search`
4. Install the required packages: `pip install -r requirements.txt`

## Running the App

1. Run the app: `streamlit run app.py`
2. Open your browser and go to the URL displayed in the terminal, e.g. http://localhost:8501

Usage
Enter a search term in the text input field to search for security audits
Press Enter to display the search results
Click on the "Save" button next to an audit to add it to the saved audits list in the sidebar
To remove a saved audit, click the "Remove" button next to the audit in the sidebar
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

License
[MIT](https://choosealicense.com/licenses/mit/)
