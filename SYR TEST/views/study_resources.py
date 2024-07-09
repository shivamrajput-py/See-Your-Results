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



study_mtitle = st.empty()

with study_mtitle:
    st.write(f"""
            <h2 style="text-align: center; align-items: center; padding-top: 0px; padding-botton: 0px;
            "><span style="color: {color};"></span>STUDY MATERIALS</h2>
            """, unsafe_allow_html=True)

st.write(f"""
            <h6 style="
            text-align: center;
            align-items: center;
            font-size: 13px;
            ">WE ARE WORKING ON ADDING BEST RESOURCES, IT IS TAKING TIME BUT WILL MAKE SURE TO COMPLETE UPLOADING ALL THE IMPORTANT RESOURCES BEFORE THIS MIDSEMS!</h6>
            """,
         unsafe_allow_html=True)

st.markdown("---")

s1, s2, s3, s4 = st.columns(4)

st.markdown("---")

with open("DATA_MAIN1.json", 'r') as fl:
    DATA = json.load(fl)

with s1: RESOURCE_BRNCH = st.selectbox("CHOOSE BRANCH: ", shortf_branch27.values(), placeholder='BRANCH')

if RESOURCE_BRNCH:
    RESOURCE_BRNCH = shortf_branch27REV[RESOURCE_BRNCH]
    RESOURCE_SEM = "2"
    with study_mtitle:
        st.write(f"""
                <h2 style="text-align: center; align-items: center; padding-top: 5px; padding-botton: 5px
                "><span style="color: {color};"></span>{RESOURCE_BRNCH} SEM{RESOURCE_SEM} STUDY MATERIALS</h2>
                """, unsafe_allow_html=True)

    if RESOURCE_BRNCH in DATA[0].keys():
        with s2:
            RESOURCE_SEM = st.selectbox("CHOOSE SEMESTER: ", DATA[0][RESOURCE_BRNCH].keys(), placeholder='SEMEMSTER',
                                        index=1)
        if RESOURCE_SEM:
            with s3:
                RESOURCE_SUBJECT = st.selectbox("CHOOSE SUBJECT: ", DATA[0][RESOURCE_BRNCH][RESOURCE_SEM].keys(),
                                                placeholder='SUBJECT')

            with study_mtitle:
                st.write(f"""
                        <h2 style="text-align: center; align-items: center; padding-top: 5px; padding-botton: 5px
                        "><span style="color: {color};">| {RESOURCE_BRNCH} | SEM{RESOURCE_SEM} | </span>STUDY MATERIAL</h2>
                        """, unsafe_allow_html=True)

            if RESOURCE_SUBJECT:
                with s4:
                    RESOURCE_TYPE = st.selectbox("CHOOSE TYPE: ", ['PYQ', 'NOTES', 'PLAYLISTS', 'ASSIGNMENTS', 'BOOKS'],
                                                 index=0, placeholder='TYPE')
                RESOURCE_SUBCODE = DATA[0][RESOURCE_BRNCH][RESOURCE_SEM][RESOURCE_SUBJECT]
                if RESOURCE_SUBCODE != "NONE":
                    with open('DATA_MAIN2.json', 'r') as fl2:
                        DATA2 = json.load(fl2)

                    if RESOURCE_TYPE:
                        material = find(RESOURCE_SUBCODE, RESOURCE_TYPE, True)
                        if material == False:
                            st.markdown("<br><br>", unsafe_allow_html=True)
                            st.warning(
                                f"SORRY :< CURRENTLY WE DON'T HAVE ANY RESOURCES RELATED TO [ {RESOURCE_BRNCH} | SEM{RESOURCE_SEM} | {RESOURCE_SUBJECT} ]")
                            st.warning(
                                f"WE ARE WORKING ON ADDING MORE BEST RESOURCES, IT WILL TAKE TIME! WE HAVE JUST STARTED WITH THIS 'RESOURCES' PART.")
                        else:
                            st.markdown("<br>", unsafe_allow_html=True)

                            last_Rest, no_of_row = len(material) % 3, len(material) // 3 + 1
                            if last_Rest == 0: no_of_row -= 1

                            if len(material) > 3:
                                for i in range(no_of_row):
                                    if i + 1 != no_of_row:
                                        bt1, bt2, bt3 = st.columns(3)
                                        with bt1:
                                            st.markdown(
                                                f'''<a class="social1_" href="{list(material.values())[0 + (3 * i)]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[0 + 3 * i]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[0 + 3 * i]}</span></button>''',
                                                unsafe_allow_html=True)
                                        with bt2:
                                            st.markdown(
                                                f'''<a class="social1_" href="{list(material.values())[1 + (3 * i)]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[1 + 3 * i]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[1 + 3 * i]}</span></button>''',
                                                unsafe_allow_html=True)
                                        with bt3:
                                            st.markdown(
                                                f'''<a class="social1_" href="{list(material.values())[2 + (3 * i)]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[2 + 3 * i]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[2 + 3 * i]}</span></button>''',
                                                unsafe_allow_html=True)
                                    else:
                                        if last_Rest == 1:
                                            bt1, bt2, bt3 = st.columns(3)
                                            with bt1:
                                                st.markdown(
                                                    f'''<a class="social1_" href="{list(material.values())[-1]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[-1]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[-1]}</span></button>''',
                                                    unsafe_allow_html=True)
                                        elif last_Rest == 2:
                                            bt1, bt2, bt3 = st.columns(3)
                                            with bt1:
                                                st.markdown(
                                                    f'''<a class="social1_" href="{list(material.values())[-2]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[-2]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[-2]}</span></button>''',
                                                    unsafe_allow_html=True)
                                            with bt2:
                                                st.markdown(
                                                    f'''<a class="social1_" href="{list(material.values())[-1]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[-1]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[-1]}</span></button>''',
                                                    unsafe_allow_html=True)

                            else:
                                if len(material) == 3:
                                    bt1, bt2, bt3 = st.columns(3)
                                    with bt1:
                                        st.markdown(
                                            f'''<a class="social1_" href="{list(material.values())[0]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[0]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[0]}</span></button>''',
                                            unsafe_allow_html=True)
                                    with bt2:
                                        st.markdown(
                                            f'''<a class="social1_" href="{list(material.values())[1]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[1]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[1]}</span></button>''',
                                            unsafe_allow_html=True)
                                    with bt3:
                                        st.markdown(
                                            f'''<a class="social1_" href="{list(material.values())[2]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[2]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[2]}</span></button>''',
                                            unsafe_allow_html=True)
                                elif len(material) == 2:
                                    bt1, bt2, bt3 = st.columns(3)
                                    with bt1:
                                        st.markdown(
                                            f'''<a class="social1_" href="{list(material.values())[0]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[0]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[0]}</span></button>''',
                                            unsafe_allow_html=True)
                                    with bt2:
                                        st.markdown(
                                            f'''<a class="social1_" href="{list(material.values())[1]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[1]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[1]}</span></button>''',
                                            unsafe_allow_html=True)

                                elif len(material) == 1:
                                    bt1, bt2, bt3 = st.columns(3)
                                    with bt1:
                                        st.markdown(
                                            f'''<a class="social1_" href="{list(material.values())[0]}"><button class="button-res" type="button"><span class="text">{list(material.keys())[0]}</span><span class="alt-text">{RESOURCE_SUBJECT}<br>{list(material.keys())[0]}</span></button>''',
                                            unsafe_allow_html=True)


                else:
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    st.warning(
                        f"SORRY :< CURRENTLY WE DON'T HAVE ANY RESOURCES RELATED TO [ {RESOURCE_BRNCH} | SEM{RESOURCE_SEM} | {RESOURCE_SUBJECT} ]")
                    st.warning(
                        f"WE ARE WORKING ON ADDING MORE BEST RESOURCES, IT WILL TAKE TIME! WE HAVE JUST STARTED WITH THIS 'RESOURCES' PART.")

    else:
        st.warning(f"SORRY, SOME PROBLEM OCCURED :< OR MAYBE WE DO NOT HAVE RESOURCES RELATED TO THIS BRANCH!")

