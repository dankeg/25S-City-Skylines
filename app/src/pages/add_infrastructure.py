import streamlit as st
import requests
from modules.nav import SideBarLinks

st.title('Log a Completed Maintenance Task')
SideBarLinks()

response = requests.get("http://web-api:4000/issue-names")

if response.status_code == 200:
    issue_options = response.json()

    if not issue_options:
        st.warning("No available issues to log maintenance for.")
        st.stop()

    issue_map = {issue['issue_type']: issue['issue_id'] for issue in issue_options}
    selected_issue_name = st.selectbox("Choose Issue Type", list(issue_map.keys()))
    selected_issue_id = issue_map[selected_issue_name]

    description = st.text_area("Maintenance Description")

    if st.button("Submit Maintenance Log"):
        maintenance = {
            'issue_id': selected_issue_id,
            'description': description,
        }
        post_response = requests.post("http://web-api:4000/updatinglog", json=maintenance)
        if post_response.status_code == 201:
            st.success("Maintenance log added and issue marked as completed!")
        else:
            st.error(f"Failed to log maintenance: {post_response.text}")
else:
    st.error("Unable to load issue types. Please try again later.")
