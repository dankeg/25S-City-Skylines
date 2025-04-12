import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Sustainability Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View EV Usage Alongside Air Quality Metrics', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/002a_EV_Air_Quality_Viz.py')

if st.button('Add New Building Energy Consumption Point to CO2 Emissions Data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/002b_Add_Building_CO2.py')

if st.button('Update Water Quality Sensor Status', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/002c_Update_Sensor_Status.py')