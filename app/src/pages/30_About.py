import streamlit as st
from modules.nav import SideBarLinks

def about_page():    
    SideBarLinks()
    
    st.title("🏙️ About City Skylines")
    
    st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3", 
             width=800)
    
    st.header("Transforming Urban Management with Data")
    
    st.markdown("""
    **City Skylines** is a next-generation smart city platform that revolutionizes how cities are planned, 
    maintained, and optimized. Our integrated solution brings together the essential tools urban professionals 
    need to build sustainable, efficient, and responsive communities.
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Our Mission")
        st.markdown("""
        - Eliminate data silos in urban management
        - Replace manual processes with real-time analytics
        - Enable predictive infrastructure planning
        - Foster sustainable city development
        """)
        
    with col2:
        st.subheader("✨ Key Features")
        st.markdown("""
        - Unified dashboard for all urban systems
        - IoT-powered infrastructure monitoring        
        - Collaborative planning tools
        - Sustainability performance tracking
        """)
    
    st.divider()
    
    st.subheader("👥 Designed For Urban Professionals")
    
    roles = {
        "City Planners": "Visualize development impacts and optimize zoning",
        "Sustainability Analysts": "Track emissions and green initiatives",
        "Infrastructure Managers": "Monitor assets and predict maintenance needs",
        "System Administrators": "Configure permissions and data integrations"
    }
    
    for role, desc in roles.items():
        st.markdown(f"**{role}** - {desc}")  

if __name__ == "__main__":
    about_page()