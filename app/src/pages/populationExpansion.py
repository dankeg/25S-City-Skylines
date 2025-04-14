import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000"
REGIONS_ENDPOINT = f"{API_BASE_URL}/regions"

SideBarLinks()

def get_region_data():
    """Fetch region data from API"""
    try:
        response = requests.get(REGIONS_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching region data: {e}")
        return []

def calculate_future_population(current_pop, years, growth_rate):    
    return round(current_pop * (1 + growth_rate/100) ** years)

def main():
    st.title("Smart City Population Projections")
    st.markdown("Predict future population growth to plan urban infrastructure needs.")
        
    regions = get_region_data()
    
    if not regions:
        st.warning("No region data available. Please check your API connection.")
        return
        
    st.subheader("Current Population by Region")
    current_df = pd.DataFrame(regions)[['name', 'population']]
    st.dataframe(current_df.sort_values('population', ascending=False))
        
    st.subheader("📈 Projection Parameters")
    col1, col2 = st.columns(2)
    with col1:
        years = st.slider("Years to project", 1, 50, 10)
    with col2:
        growth_rate = st.slider("Annual growth rate (%)", 0.1, 10.0, 2.5, step=0.1)
        
    if st.button("Calculate Future Population", type="primary"):
        projection_data = []
        for region in regions:
            future_pop = calculate_future_population(
                region['population'], 
                years, 
                growth_rate
            )
            projection_data.append({
                'Region': region['name'],
                'Current Population': region['population'],
                'Future Population': future_pop,
                'Growth': future_pop - region['population']                
            })
        
        projection_df = pd.DataFrame(projection_data)
        
        st.subheader(f"📊 Projected Population in {years} years at {growth_rate}% growth")
                
        total_current = projection_df['Current Population'].sum()
        total_future = projection_df['Future Population'].sum()
        col1, col2 = st.columns(2)
        col1.metric("Total Current Population", f"{total_current:,}")
        col2.metric("Total Future Population", f"{total_future:,}", 
                   f"{(total_future/total_current-1)*100:.1f}%")
                
        st.dataframe(projection_df.sort_values('Growth', ascending=False))
                
        st.bar_chart(
            projection_df.set_index('Region')[['Current Population', 'Future Population']],
            height=500
        )

if __name__ == "__main__":
    main()