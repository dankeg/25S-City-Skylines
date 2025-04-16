import logging
import requests
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
from datetime import datetime
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Monitoring Dashboard")
st.subheader(f"Welcome, {st.session_state['first_name']}!")

st.divider()
st.markdown("### 🛠️ Monitoring Configurations")

configs = requests.get("http://web-api:4000/sys/monitoring-config").json()
configs_df = pd.DataFrame(configs)


def on_config_change():
    edited_data = st.session_state.config_table

    if edited_data.get("edited_rows"):
        for row_index, changes in edited_data["edited_rows"].items():
            row_index = int(row_index)
            updated = configs_df.iloc[row_index].copy()
            for col, new_value in changes.items():
                updated[col] = new_value
            row_dict = updated.to_dict()
            config_id = row_dict["config_id"]
            requests.put(
                f"http://web-api:4000/sys/monitoring-config/{config_id}", json=row_dict
            )

    for row in edited_data.get("added_rows", []):
        requests.post("http://web-api:4000/sys/monitoring-config", json=row)

    for idx in edited_data.get("deleted_rows", []):
        config_id = configs_df.iloc[int(idx)]["id"]
        requests.delete(f"http://web-api:4000/sys/monitoring-config/{config_id}")


st.data_editor(
    configs_df,
    key="config_table",
    num_rows="dynamic",
    use_container_width=True,
    on_change=on_config_change,
    hide_index=True,
)

st.divider()
st.markdown("### ⚠️ Incidents by Monitoring Config")

monitored_incidents = requests.get("http://web-api:4000/sys/monitored-incidents").json()
monitored_incidents = pd.DataFrame(monitored_incidents)

monitored_incidents["start_time"] = pd.to_datetime(monitored_incidents["start_time"])
monitored_incidents["end_time"] = pd.to_datetime(monitored_incidents["end_time"])

for config_id, group in monitored_incidents.groupby("config_id"):
    config_name = group["job"].iloc[0]

    with st.expander(f"🔧 {config_name} (ID: {config_id})"):
        display_cols = ["incident_id", "start_time", "end_time", "severity", "status"]
        if all(col in group.columns for col in display_cols):
            st.dataframe(
                group[display_cols].sort_values("start_time"), use_container_width=True
            )
        else:
            st.write("⚠️ Incomplete incident data for this config.")
st.divider()

incident_response = requests.get("http://web-api:4000/sys/incidents").json()
incident_df = pd.DataFrame(incident_response)
st.markdown("### 📈 Incident Gantt Timeline")

incident_df["start_time"] = pd.to_datetime(incident_df["start_time"])
incident_df["end_time"] = pd.to_datetime(incident_df["end_time"])

if not incident_df.empty:
    fig, ax = plt.subplots(figsize=(10, 5))

    for i, row in incident_df.iterrows():
        color = (
            "tab:red"
            if row["severity"] == "high"
            else "tab:orange" if row["severity"] == "medium" else "tab:green"
        )
        ax.barh(
            y=row["incident_id"],
            width=(row["end_time"] - row["start_time"]),
            left=row["start_time"],
            color=color,
            edgecolor="black",
            alpha=0.7,
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("Incident ID")
    ax.set_title("Incident Duration per Config")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.invert_yaxis()
    ax.grid(True)

    st.pyplot(fig)
else:
    st.info("No incident data available to render Gantt timeline.")
