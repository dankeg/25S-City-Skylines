import logging
import pandas as pd
import streamlit as st
import requests
import matplotlib.pyplot as plt
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Setting up logger
logger = logging.getLogger(__name__)

# Sidebar nav
SideBarLinks()

st.header("EV Infrastructure and Air Quality Metrics Data")
st.write(f"### Hi, {st.session_state.get('first_name', 'User')}.")

# Loading EV + Air Quality data
api_url = "http://web-api-test:4000/s/ev-air-dashboard"

try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)

    # Converting columns to appropriate data types
    df['energy_consumption'] = pd.to_numeric(df['energy_consumption'], errors='coerce')
    df['usage_level'] = pd.to_numeric(df['usage_level'], errors='coerce')
    df['AQI'] = pd.to_numeric(df['AQI'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    st.dataframe(df)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Plot: Energy Consumption vs AQI
fig, ax = plt.subplots()
ax.scatter(df['energy_consumption'], df['AQI'], alpha=0.7, color='green')
ax.set_xlabel("Energy Consumption (kWh)")
ax.set_ylabel("Air Quality Index (AQI)")
ax.set_title("Energy Consumption vs AQI")
st.pyplot(fig)
