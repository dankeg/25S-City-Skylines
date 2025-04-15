import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"
PROJECTS_ENDPOINT = f"{API_BASE_URL}/project-locations"

SideBarLinks()

def get_project_data():
    """Fetch project location data from API"""
    try:
        response = requests.get(PROJECTS_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching project data: {e}")
        return []

def main():
    st.title("🗺️ Smart City Projects Map")
    st.markdown("Interactive map of all proposed and ongoing smart city initiatives")
        
    projects = get_project_data()
    
    if not projects:
        st.warning("No project data available. Please check your API connection.")
        return
        
    df = pd.DataFrame(projects)
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
        
    status_colors = {
        'proposed': [255, 140, 0],  
        'inProgress': [0, 191, 255],  
        'completed': [50, 205, 50]  
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
    
    tooltip = {
        "html": "<b>Project:</b> {name}<br/>"
                "<b>Status:</b> {status}<br/>"
                # "<b>Budget:</b> ${budget:,.2f}<br/>"
                "<b>Sustainability Score:</b> {sustainabilityScore}/100<br/>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
    
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    ))
        
    st.subheader("Project Details")
    st.dataframe(df[['name', 'status', 'budget', 'sustainabilityScore']])

if __name__ == "__main__":
    main()