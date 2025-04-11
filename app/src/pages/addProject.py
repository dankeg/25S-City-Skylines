import streamlit as st
import requests
from modules.nav import SideBarLinks

st.title('Add a Project')
SideBarLinks()


regions = requests.get("http://web-api:4000/regions").json()
departments = requests.get("http://web-api:4000/departments").json()

name = st.text_input("Project Name")
status = st.selectbox("Status", ['proposed', 'inProgress', 'completed'])
budget = st.number_input("Budget")
description = st.text_area("Description")
sustainability = st.number_input("Sustainability Score (0-100)", min_value=0, max_value=100)
time = st.number_input("Time to Complete (months)", min_value=1)

dept_options = {d['department_id']: d['name'] for d in departments}

dept_id = st.selectbox(
    "Department",
    options=list(dept_options.keys()),
    format_func=lambda id: dept_options[id]
)

region_dict = {r['region_id']: r['name'] for r in regions}

region_id = st.selectbox(
    "Region",
    options=list(region_dict.keys()), 
    format_func=lambda id: region_dict[id]  
)

if st.button("Add Project"):
    project = {
        'name': name,
        'status': status,
        'budget': budget,
        'description': description,
        'sustainabilityScore': sustainability,
        'timeToCompletion': time,
        'region_id': region_id,
        'department_id': dept_id
    }
    response = requests.post("http://web-api:4000/projects", json=project)
    if response.status_code == 201:
        st.success("Project added!")
    else:
        st.error("Failed to add project")