import streamlit as st
import requests
from modules.nav import SideBarLinks

st.title('Add a Maintenance')
SideBarLinks()

issue_id = st.number_input("IssueId")
log_id = st.number_input("LogId")
description = st.text_area("Description")

if st.button("Add Maintenance Log"):
    maintenance = {
        'issue_id': issue_id,
        'log_id': log_id,
        'description': description
    }
    response = requests.post("http://web-api:4000/updatinglog", json=maintenance)
    if response.status_code == 201:
        st.success("Maintenance Log added!")
    else:
        st.error("Failed to add Maintenance Log")