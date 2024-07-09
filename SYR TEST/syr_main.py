import streamlit as st

st.set_page_config(layout='wide', page_title='DTU Student Profile', page_icon='🎓', initial_sidebar_state='expanded')


# --- PAGE SETUP ---
profile_page = st.Page(
    "views/student_profile.py",
    title="STUDENT PROFILE",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "views/ranks_and_results.py",
    title="RANK AND RESULTS",
    icon=":material/bar_chart:",
)
project_2_page = st.Page(
    "views/placement_stats.py",
    title="PLACEMENTS",
    icon="",
)

project_3_page = st.Page(
    "views/study_resources.py",
    title="STUDY RESOURCES",
    icon="",
)

project_4_page = st.Page(
    "views/sgpa_calculator.py",
    title="SGPA CALCULATOR",
    icon="",
)

project_5_page = st.Page(
    "views/about.py",
    title="ABOUT US",
    icon="",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "LIVE": [profile_page, project_1_page, project_2_page ],
        "Projects": [project_3_page, project_4_page, project_5_page],
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")
st.sidebar.text("Made with ❤️ by Sven")


# --- RUN NAVIGATION ---
pg.run()