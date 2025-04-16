import logging
import requests
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import math
from modules.nav import SideBarLinks

SideBarLinks()

st.title("User Tickets and Requests")
st.subheader(f"Welcome, {st.session_state['first_name']}!")

results = requests.get("http://web-api:4000/sys/user-tickets").json()
user_tickets_df = pd.DataFrame(results)

results = requests.get("http://web-api:4000/sys/users").json()
users_df = pd.DataFrame(results)

user_email_to_id = dict(zip(users_df["email"], users_df["user_id"]))
id_to_email = dict(zip(users_df["user_id"], users_df["email"], ))

user_tickets_df["filer_id"] = user_tickets_df["filer_id"].map(id_to_email)
user_tickets_df["assignee_id"] = user_tickets_df["assignee_id"].map(id_to_email)


def on_modification_callback():
    edited_data = st.session_state.user_tickets

    if edited_data.get("edited_rows"):
        for row_index, changes in edited_data["edited_rows"].items():
            row_index = int(row_index)

            for col, new_value in changes.items():
                user_tickets_df.at[row_index, col] = new_value

            row_dict = user_tickets_df.iloc[row_index].to_dict()

            for key, value in row_dict.items():
                if isinstance(value, float) and math.isnan(value):
                    row_dict[key] = None

            row_dict["assignee_id"] = user_email_to_id.get(row_dict["assignee_id"])
            row_dict["filer_id"] = user_email_to_id.get(row_dict["filer_id"])

            ticket_id = row_dict.get("ticket_id")
            requests.put(
                f"http://web-api:4000/sys/user-tickets/{ticket_id}", json=row_dict
            )

    for row in edited_data.get("added_rows", []):
        if "filer_id" in row:
            row["filer_id"] = user_email_to_id.get(row["filer_id"])

        if "assignee_id" in row:
            row["assignee_id"] = user_email_to_id.get(row["assignee_id"])
        requests.post("http://web-api:4000/sys/user-tickets", json=row)

    for idx in edited_data.get("deleted_rows", []):
        ticket_id = user_tickets_df.iloc[int(idx)]["ticket_id"]
        requests.delete(f"http://web-api:4000/sys/user-tickets/{ticket_id}")


st.divider()
st.markdown("### Current Tickets")

column_config = {
    "status": st.column_config.SelectboxColumn(
        "Status",
        help="Select ticket status",
        options=["open", "in-progress", "closed"],
        required=True,
    ),
    "filer_id": st.column_config.SelectboxColumn(
        "User",
        help="Select ticket status",
        options=list(user_email_to_id.keys()),
        required=True,
    ),
    "assignee_id": st.column_config.SelectboxColumn(
        "Assignee",
        help="Select ticket status",
        options=list(user_email_to_id.keys()),
    ),
    "title": st.column_config.TextColumn(
        "title",
        required=True,
    ),
    
}

st.data_editor(
    user_tickets_df,
    key="user_tickets",
    num_rows="dynamic",
    column_config=column_config,
    on_change=on_modification_callback,
    use_container_width=True,
    hide_index=True,
    column_order=["title","description","status", "filer_id", "assignee_id"]
)

st.divider()
st.markdown("### 📊 Ticket Status Overview")

status_counts = user_tickets_df["status"].value_counts()

fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
ax.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor": "white"},
)
ax.set_title("User Ticket Status")
ax.axis("equal")

_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    st.pyplot(fig, use_container_width=False)
