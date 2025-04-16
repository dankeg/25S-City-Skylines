import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from datetime import datetime
from modules.nav import SideBarLinks

SideBarLinks()

st.header("💧 Water Sensor Status Overview")
st.write(f"### Hi, {st.session_state.get('first_name', 'User')}.")
api_url_get = "http://web-api-test:4000/s/water-sensors"

try:
    response = requests.get(api_url_get)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    def highlight_status(row):
        color = ''
        if row['status'].lower() == 'decommissioned':
            color = 'background-color: #ffcccc'
        elif row['status'].lower() == 'inactive':
            color = 'background-color: #fff3cd'
        return ['' if col != 'status' else color for col in row.index]

    styled_df = df.style.apply(highlight_status, axis=1)
    st.dataframe(styled_df)

except Exception as e:
    st.error(f"Error loading sensor data: {e}")
    st.stop()

st.subheader("🔧 Update Sensor Status")

with st.form("update_sensor"):
    col1, col2 = st.columns(2)

    with col1:
        sensor_id = st.selectbox("Sensor ID", df['sensor_id'].unique())
        current_status = df[df['sensor_id'] == sensor_id]['status'].values[0]

        if current_status.lower() == "inactive":
            color = "#e6b800"
        elif current_status.lower() == "decommissioned":
            color = "#cc0000"
        else:
            color = "#28a745"

        st.markdown(
            f"**Current status:** <span style='color:{color}'>{current_status}</span>",
            unsafe_allow_html=True
        )

    with col2:
        new_status = st.selectbox("New Status", ["Active", "Inactive", "Decommissioned"])

    submit = st.form_submit_button("Update Status")

    if submit:
        payload = {
            "sensor_id": sensor_id,
            "status": new_status
        }

        try:
            put_res = requests.put("http://web-api-test:4000/s/water-sensor-status", json=payload)
            if put_res.status_code == 200:
                st.success("Sensor status updated successfully!")
            else:
                st.error(f"Error: {put_res.status_code} - {put_res.text}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")
