import csv

import streamlit
import streamlit as st
import json
import pandas as pd
import plotly_express as px
from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
import os
import datetime
import statistics

import warnings
warnings.filterwarnings('ignore')
countedview = 0
WEBONSERVER = True

grdpoint = {
    'O':10, 'A+':9, 'A':8, 'B+':7, 'B':6, 'C':5, 'P':4,'F': 0}

shortf_branch26 = {
    'CO': 'Computer Science',
    'IT': 'Information Technology',
    'SE': 'Software Engineering',
    'MC': 'Mathematics and Computing',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electrical Engineering',
    'EP': 'Engineering Physics',
    'ME': 'Mechanical Engineering',
    'AE': 'Automotive Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Chemical Engineering',
    'PE': 'Production Engineering',
    'EN': 'Environmental Engineering',
    'BT': 'Bio-Technology'
}

shortf_branch26REV = dict((v,k) for k,v in shortf_branch26.items())

shortf_branch27 = {
    'CS': 'Computer Science',
    'IT': 'Information Technology',
    'SE': 'Software Engineering',
    'MC': 'Mathematics and Computing',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electrical Engineering',
    'EP': 'Engineering Physics',
    'ME': 'Mechanical Engineering',
    'AE': 'Automotive Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Chemical Engineering',
    'PE': 'Production Engineering',
    'EN': 'Environmental Engineering',
    'BT': 'Bio-Technology'
}



shortf_branch27REV = dict((v,k) for k,v in shortf_branch27.items())


placem_branch_name = {
    'EP': 'Engineering Physics',
    'AE': 'Mechanical Engineering with Specialization in Automotive',
    'CS': 'Computer Engineering',
    'IT': 'Information Technology',
    'MC': 'Mathematics and Computing',
    'CO': 'Computer Engineering',
    'SE': 'Software Engineering',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electrical Engineering',
    'BT': 'Bio-Technology',
    'EN': 'Environmental Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Polymer Science and Chemical Technology',
    'PE': 'Production and Industrial Engineering',
    'ME': 'Mechanical Engineering'
}


# color_discrete_sequence=['#0573ff']

# st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='DTU Student Profile', page_icon='🎓')

color = '#1F51FF' # USE FOR HIGHLIGHTING A SPECIFIC WORD
other= False

with open('style.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# FOR LOADING THE ANIMATION !!
def load_lottieurl(isjson: bool, url_or_path: str):
    if isjson:
        with open(url_or_path, 'r') as fl:
            return json.loads(fl.read())
    else:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


def find(SUBC: str, TYPE: str, sendsorted=True) -> dict:
    # TODO: FINDING MORE SUBJECT CODE GROUPS AND ADDING THEM INTO THIS
    SUBJECT_GROUP_STR = [" CO101 | CO102 | CO116 | CO105 ", ]

    for sub_grp in SUBJECT_GROUP_STR:
        if SUBC in sub_grp:
            SUBC = sub_grp

    with open(r'DATA_MAIN2.json', 'r') as fl:
        doc = json.load(fl)

    if SUBC in doc[0][TYPE].keys():
        req_dic = {}
        if sendsorted:
            for key in doc[0][TYPE][SUBC].keys():
                if doc[0][TYPE][SUBC][key]!="":
                   req_dic[key] = doc[0][TYPE][SUBC][key]

            return req_dic
        else:
            return doc[0][TYPE][SUBC]
    else:
        return False



# VIEW COUNTING
if countedview == 0 and WEBONSERVER:
    countedview += 1
    with open('user_webViewsData.txt', 'a') as fl:
        fl.write(f"""USER AT {datetime.datetime.now()} CLICKED "ABOUT" (VIEW COUNTED)\n""")
        fl.flush()

lc, rc = st.columns([1.3, 1])

with rc:
    st.write('<h6>This Website is Developed and Maintained By ME.</h6>', unsafe_allow_html=True)
    l_, m_, r_ = st.columns([5, 2.5, 2.5])

    st_lottie(
        load_lottieurl(True, "./animation/boy_workingBack.json"),
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=None,
        width=530,
        key=None,
    )

    with l_:
        st.write(f"""
                        <h4>Hey, SHIVAM Here<br>Engineering Physics 2027</h4>
                        """,
                 unsafe_allow_html=True)

    with m_:
        st.markdown('######')
        st.markdown(
            '''<a id="social1" href="https://www.instagram.com/shivammm20_/"><button class="button-62" type="button">INSTA</button>''',
            unsafe_allow_html=True)

    with r_:
        st.markdown('######')
        st.markdown(
            '''<a id="social2" href="https://www.linkedin.com/in/shivam-rajput-3928a328a/"><button class="button-18" type="button">LINKEDIN</button>''',
            unsafe_allow_html=True)

with lc:
    st.write(f"""
    <h1 class="nametit">Your Education<br>Dashboard<br><span class="nametitm">DTU RESULTS</span></h1>
            <br>""", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    st.write(f"""
        <h3 class="about">MORE <span style="color: #1F51FF;">FEATURES</span> TO COME, IN FURTHER UPDATES</h3>
        <h6 class="about">- 2nd Sem results ? YES I WILL UPDATE, After Results, ASAP!</h6>
        <h6 class="about">- What about 2025 Results etc? YES I am going to add them too, it will take time. </h6>
        <h6 class="about">- Study Material and Resources that will help during exams</h6>
        <h6 class="about">- Other than this, Suggest me what more should i add ?</h6>
        """,
             unsafe_allow_html=True)

    st.markdown('<br><br><br>', unsafe_allow_html=True)

# st.warning("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF'S, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR YOU FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE CONTACT ME, I WILL SOLVE IT ASAP!")

