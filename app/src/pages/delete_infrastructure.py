import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"
ALL_INFRA_ENDPOINT = f"{API_BASE_URL}/infrastructure_types"
ALL_INFR_DEL_ENDPOINT = f"{API_BASE_URL}/infrastructure_type"

SideBarLinks()

def get_all_infra():
    """Fetch project location data from API"""
    try:
        response = requests.get(ALL_INFRA_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching project data: {e}")
        return []

def main():
    st.title("All Infrastructure Types ") 
    st.markdown("All Infrastructure Type that can be deleted")
        
    infra_types = get_all_infra()
    
    if not infra_types:
        st.warning("No Infractures types available. Please check your API connection.")
        return
        
    df = pd.DataFrame(infra_types)

    st.subheader("Delete a Infrastructure Type")

    for index, row in df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 2])
        
        with col1:
            st.write(row['type_id'])
        with col2:
            st.write(row['issue_id'])
        with col3:
            st.write(row['type'])
        with col4:
            st.write(row['location_id'])
        with col5:
            st.write(row['priority'])
        with col6:
            if st.button("Delete", key=f"delete_{row['type_id']}"):
                try:
                    response = requests.delete(f"{ALL_INFR_DEL_ENDPOINT}/{row['issue_id']}")
                    if response.status_code == 200:
                        st.success(f"Infrastructure Deleted '{row['type_id']}' successfully.")
                    else:
                        st.error(f"Failed to delete Infrastructure types '{row['type_id']}'.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error during deletion: {e}")

if __name__ == "__main__":
    main()