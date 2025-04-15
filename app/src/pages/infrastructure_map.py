import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"
ACTIVE_WORK_ORDERS_ENDPOINT = f"{API_BASE_URL}/active-work-orders"

SideBarLinks()

def get_work_orders_data():
    """Fetch project location data from API"""
    try:
        response = requests.get(ACTIVE_WORK_ORDERS_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching project data: {e}")
        return []

def main():
    st.title("Active Work Orders Map")
    st.markdown("Interactive map of all active work orders that need to be adressed")
        
    work_orders = get_work_orders_data()
    
    if not work_orders:
        st.warning("No project data available. Please check your API connection.")
        return
        
    df = pd.DataFrame(work_orders)
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')


    """
     "crew_id": 3,
    "crew_name": "Capital Clean-Up Services",
    "description": "Request for revitalization of a neglected neighborhood.",
    "issue_id": 18,
    "issue_type": "Unmaintained parks and gardens",
    "latitude": "39.73400000",
    "longitude": "-105.02590000",
    "priority": "Critical",
    "status": "Open"
    """
        
    status_colors = {
        'Open': [255, 140, 0],  
        'In Progress': [0, 191, 255],  
        'Resolved': [50, 205, 50]  
    }
        
    df['color'] = df['status'].apply(lambda x: status_colors.get(x, [200, 200, 200]))
        
    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=10,
        pitch=40
    )
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[longitude, latitude]',
        get_color='color',
        get_radius=200,
        pickable=True
    )
   
    
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[layer]
    ))

        # Legend for dot colors
    st.markdown("""
    <div style='padding: 10px; border: 1px solid #ddd; border-radius: 5px; width: fit-content; background-color: #f9f9f9'>
        <strong>🗝️ Legend:</strong><br>
        <div style='margin-bottom: 5px;'>
            <span style='display: inline-block; width: 15px; height: 15px; background-color: rgb(255, 140, 0); margin-right: 5px;'></span>
            Open Work Order
        </div>
        <div>
            <span style='display: inline-block; width: 15px; height: 15px; background-color: rgb(0, 191, 255); margin-right: 5px;'></span>
            In Progress Work Order
        </div>
    </div>
    """, unsafe_allow_html=True)

        
    st.subheader("active work orders Table")
    st.dataframe(df[['crew_name', 'status', 'description', 'priority', 'issue_type']])

if __name__ == "__main__":
    main()