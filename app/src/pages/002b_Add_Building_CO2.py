import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from datetime import datetime
from modules.nav import SideBarLinks

SideBarLinks()

st.header("CO₂ Emissions from Building Sources")
st.write(f"### Hi, {st.session_state.get('first_name', 'User')}.")
api_url = "http://web-api-test:4000/s/co2-building-emissions"

try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['emission_level'] = pd.to_numeric(df['emission_level'], errors='coerce')

    st.dataframe(df)

except Exception as e:
    st.error(f"Error loading emissions data: {e}")
    st.stop()

st.subheader("➕ Add New CO₂ Emission Data for A Building!")

with st.form("add_emission"):
    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("Source", ["Commercial Building", "Building Meter", "Deforestation", "Energy Production",
        "Land Use Changes"])
        emission_level = st.number_input("Emission Level (kg)", min_value=0.0, step=0.1)
        location_id = st.number_input("Location ID", min_value=1, step=1)

    with col2:
        building_id = st.number_input("Building ID", min_value=0, step=1)
        date = st.date_input("Date", value=datetime.now().date())
        time = st.time_input("Time", value=datetime.now().time())
        timestamp = datetime.combine(date, time)

    submit = st.form_submit_button("Submit Entry")

    if submit:
        payload = {
            "source": source,
            "emission_level": emission_level,
            "location_id": location_id,
            "timestamp": timestamp.isoformat()
        }

        if building_id != 0:
            payload["building_id"] = building_id

        try:
            post_res = requests.post(api_url, json=payload)
            if post_res.status_code == 201:
                st.success("CO₂ emission entry added successfully!")
            else:
                st.error(f"Please include valid locations and buildings!")
        except Exception as e:
            st.error(f"Please include valid locations and buildings!: {e}")
