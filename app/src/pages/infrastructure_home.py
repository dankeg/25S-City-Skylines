import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title(f"Welcome Infrastructure Managment Supervisor, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View All Active Work Orders', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/infrastructure_map.py')

if st.button('Log a Completed Maintenance Job',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/add_infrastructure.py')

if st.button('Delete an Associated Infrastructure Type',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/delete_infrastructure.py')
