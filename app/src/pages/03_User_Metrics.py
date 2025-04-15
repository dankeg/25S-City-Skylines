import logging
import requests
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import math
from modules.nav import SideBarLinks

# Sidebar navigation
SideBarLinks()

# Header
st.title("User Metrics")
st.subheader(f"Welcome, {st.session_state['first_name']}!")

# Date selection
start_date = st.date_input("Select Start Date", key="login_start_date")
end_date = st.date_input("Select End Date", key="login_end_date")

if start_date and end_date:
    if start_date > end_date:
        st.error("Start Date must be before End Date.")
    else:
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        login_response = requests.get(
            f"http://web-api:4000/sys/users/{start_str}/{end_str}"
        ).json()
        login_df = pd.DataFrame(login_response)

        if not login_df.empty and "last_login" in login_df.columns:
            login_df["last_login"] = pd.to_datetime(login_df["last_login"])
            login_df["date"] = login_df["last_login"].dt.date

            bins = pd.date_range(
                start=start_date, end=end_date + pd.Timedelta(days=1), freq="D"
            )
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.hist(login_df["last_login"], bins=bins, edgecolor="black")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Logins")
            ax.set_title("User Logins")
            st.pyplot(fig)

            total_logins = len(login_df)
            days_range = (end_date - start_date).days + 1
            avg_logins_per_day = (
                total_logins / days_range if days_range > 0 else total_logins
            )

            login_counts = login_df["date"].value_counts().sort_index()
            peak_day = login_counts.idxmax()
            peak_count = login_counts.max()

            st.markdown("### Summary Statistics")
            st.write(f"**Total Logins:** {total_logins}")
            st.write(f"**Date Range:** {start_str} to {end_str} ({days_range} days)")
            st.write(f"**Average Logins per Day:** {avg_logins_per_day:.2f}")
            st.write(f"**Peak Login Day:** {peak_day} with {peak_count} logins")

        else:
            st.info("No login data available for the selected date range.")
