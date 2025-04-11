import streamlit as st
import requests
from modules.nav import SideBarLinks

st.title('Compare Projects')
SideBarLinks()

projects = requests.get("http://web-api:4000/projects").json()
regions = {r['region_id']: r['name'] for r in requests.get("http://web-api:4000/regions").json()}
departments = {d['department_id']: d['name'] for d in requests.get("http://web-api:4000/departments").json()}

col1, col2 = st.columns(2)
with col1:
    project1 = st.selectbox("Project 1", projects, format_func=lambda p: p["name"])
with col2:
    project2 = st.selectbox("Project 2", 
                          projects, 
                          format_func=lambda p: p["name"])


if project1 and project2:
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(project1["name"])        
        st.write(f"**Budget:** ${project1['budget']}")
        st.write(f"**Department:** {project1['department_id']}")
        st.write(f"**Region:** {project1['region_id']}")
        st.write(f"**Status:** {project1['status']}")
        st.write(f"**Sustainability Score:** {project1['sustainabilityScore']}")
        st.write(f"**Time to Complete:** {project1['timeToCompletion']} months")
        st.write(f"**Description:** {project1['description']}")
        st.write(f"**Department:** {departments.get(project1['department_id'], 'N/A')}") 
        st.write(f"**Region:** {regions.get(project1['region_id'], 'N/A')}")
    with col2:
        st.subheader(project2["name"])        
        st.write(f"**Budget:** ${project2['budget']}")
        st.write(f"**Department:** {project2['department_id']}")
        st.write(f"**Region:** {project2['region_id']}")
        st.write(f"**Status:** {project2['status']}")
        st.write(f"**Sustainability Score:** {project2['sustainabilityScore']}")
        st.write(f"**Time to Complete:** {project2['timeToCompletion']} months")
        st.write(f"**Description:** {project2['description']}")
        st.write(f"**Department:** {departments.get(project2['department_id'], 'N/A')}")  
        st.write(f"**Region:** {regions.get(project2['region_id'], 'N/A')}") 