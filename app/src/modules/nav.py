# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Role of Sustainalibility Analyst ------------------------
def SustainabilityHomeNav():
    st.sidebar.page_link(
        "pages/002_Sustainability_Analyst_Home.py", label="Analyst Home", icon="🌱")


def EVStationVizNav():
    st.sidebar.page_link(
        "pages/002a_EV_Air_Quality_Viz.py", label="EV & Air Quality Viz", icon="🚗")


def AddBuildingCO2Nav():
    st.sidebar.page_link("pages/002b_Add_Building_CO2.py", label="Add Emissions Data", icon="🏭")



def UpdateWaterSensorNav():
    st.sidebar.page_link("pages/002c_Update_Sensor_Status.py", label="Update Sensor Status", icon="💧")


### ------------------------- Urban Planner Role -------------------------
def UrbanPlannerNav():
    st.sidebar.page_link(
        "pages/urbanPlannerHome.py", label="Urban Planner Home", icon="🏙️"
    )
    st.sidebar.page_link(
        "pages/compareProjects.py", label="Compare Projects", icon="📊"
    )
    st.sidebar.page_link(
        "pages/addProject.py", label="Add a Project", icon="➕"
    )
    st.sidebar.page_link(
        "pages/populationExpansion.py", label="Population Expansion", icon="🌍"
    )
    st.sidebar.page_link(
        "pages/urbanPlannerMap.py", label="Urban Planner Map", icon="🗺️"
    )

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/City_Skylines_Logo.png", width=400)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show Sustainability Links if the user is a sustainability analyst role.
        if st.session_state["role"] == "sustainability_analyst":
            SustainabilityHomeNav()
            EVStationVizNav()
            AddBuildingCO2Nav()
            UpdateWaterSensorNav()

        # If the user is an urban planner, give them access to the urban planner pages
        if st.session_state["role"] == "urbanPlanner":
            UrbanPlannerNav() 

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
