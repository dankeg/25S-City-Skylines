# import streamlit as st
# import requests
# from modules.nav import SideBarLinks

# st.title('Add a Maintenance')
# SideBarLinks()

# issue_id = st.number_input("IssueId", min_value=1, step=1)
# log_id = st.number_input("LogId", min_value=1, step=1)
# description = st.text_area("Description")

# if st.button("Add Maintenance Log"):
#     maintenance = {
#         'issue_id': int(issue_id),
#         'log_id': int(log_id),
#         'description': description
#     }
#     response = requests.post("http://web-api:4000/updatinglog", json=maintenance)
#     if response.status_code == 201:
#         st.success("Maintenance Log added!")
#     else:
#         st.error(f"Failed to add Maintenance Log: {response.text}")

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.title('Log a Completed Maintenance Task')
SideBarLinks()

# Fetch issue names
response = requests.get("http://web-api:4000/issue-names")

if response.status_code == 200:
    issue_options = response.json()

    if not issue_options:
        st.warning("No available issues to log maintenance for.")
        st.stop()

    # Dropdown: display issue_type, return issue_id
    st.write(issue_options)
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
