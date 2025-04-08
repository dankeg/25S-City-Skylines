import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Prediction with Regression')

# create a 2 column layout
col1, col2 = st.columns(2)

# add one number input for variable 1 into column 1
with col1:
  var_01 = st.number_input('Variable 01:',
                           step=1)

# add another number input for variable 2 into column 2
with col2:
  var_02 = st.number_input('Variable 02:',
                           step=1)

logger.info(f'var_01 = {var_01}')
logger.info(f'var_02 = {var_02}')

# add a button to use the values entered into the number field to send to the 
# prediction function via the REST API
if st.button('Calculate Prediction',
             type='primary',
             use_container_width=True):
  results = requests.get(f'http://api:4000/c/prediction/{var_01}/{var_02}').json()
  st.dataframe(results)
  