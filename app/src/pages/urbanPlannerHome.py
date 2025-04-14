import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title(f"Welcome Urban Planner, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Compare Projects', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/compareProjects.py')

if st.button('Add a Project',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/addProject.py')

if st.button('Population Expansion Estimator',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/populationExpansion.py')

if st.button('Urban Planner Map',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/urbanPlannerMap.py')