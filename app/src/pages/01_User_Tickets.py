import logging
import requests
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import math
from modules.nav import SideBarLinks

# Sidebar nav
SideBarLinks()

# Header
st.title("User Tickets and Requests")
st.subheader(f"Welcome, {st.session_state['first_name']}!")

# Fetch ticket data
results = requests.get("http://web-api:4000/sys/user-tickets").json()
df = pd.DataFrame(results)

if "original_user_tickets" not in st.session_state:
    st.session_state.original_user_tickets = df.copy()


# ------------------------ Data Handling Callback ------------------------ #
def on_modification_callback():
    edited_data = st.session_state.user_tickets

    st.write(edited_data)

    if edited_data["edited_rows"]:
        original_data = st.session_state.original_user_tickets
        for row_index, changes in edited_data["edited_rows"].items():
            row_index = int(row_index)
            updated_row = original_data.iloc[row_index].copy()

            for column, new_value in changes.items():
                updated_row[column] = new_value

            update_data = updated_row.to_dict()
            ticket_id = update_data["ticket_id"]

            for key, value in update_data.items():
                if value == "nan" or (isinstance(value, float) and math.isnan(value)):
                    update_data[key] = None

            requests.put(
                f"http://web-api:4000/sys/user-tickets/{ticket_id}",
                json=update_data,
            )

    if edited_data["added_rows"]:
        for new_row in edited_data["added_rows"]:
            requests.post("http://web-api:4000/sys/user-tickets", json=new_row)

    if edited_data.get("deleted_rows"):
        for row_index in edited_data["deleted_rows"]:
            row_index = int(row_index)
            ticket_id = st.session_state.original_user_tickets.iloc[row_index]["id"]
            requests.delete(f"http://web-api:4000/sys/user-tickets/{ticket_id}")


# ------------------------ Ticket Table ------------------------ #
st.divider()
st.markdown("### Current Tickets")

column_config = {
    "status": st.column_config.SelectboxColumn(
        "Status",
        help="Select ticket status",
        options=["open", "in-progress", "closed"],
        required=True,
    ),
}

st.data_editor(
    df,
    key="user_tickets",
    num_rows="dynamic",
    column_config=column_config,
    on_change=on_modification_callback,
    use_container_width=True,
    hide_index=True,
)

# ------------------------ Status Pie Chart ------------------------ #
st.divider()
st.markdown("### 📊 Ticket Status Overview")

status_counts = df["status"].value_counts()

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
