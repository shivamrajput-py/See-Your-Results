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




if countedview == 0 and WEBONSERVER:
    countedview += 1
    with open('user_webViewsData.txt', 'a') as fl:
        fl.write(f"""USER AT {datetime.datetime.now()} CLICKED "RESULTS/RANKS" (VIEW COUNTED)\n""")
        fl.flush()

lf, rt = st.columns([0.5, 3])

with lf:
    st.markdown('<br><br><br>', unsafe_allow_html=True)

    year_choosed = st.selectbox('Choose Year', ['2027', '2026'], index=0)
    if year_choosed == '2026':
        shortf_branch = shortf_branch26
    elif year_choosed == '2027':
        shortf_branch = shortf_branch27

    brnch_choosed = st.selectbox('Choose Branch', ['Cumulative'] + list(shortf_branch.values()),
                                 index=0)

    text_search = st.text_input(label="Enter Roll Number Or Name To Search Students", value="")

if brnch_choosed:
    if brnch_choosed == 'Cumulative':
        if year_choosed == '2026':
            flname, title_help = f'26_UNI_ranked_results.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking 2026'
        elif year_choosed == '2027':
            flname, title_help = f'1_UNI_ranked_results.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking 2027'
    else:
        for key in shortf_branch.keys():
            if shortf_branch[key] == brnch_choosed:
                if year_choosed == '2027':
                    flname = f'1_{key}_ranked_results.csv'
                    title_help = f'<span style="color: {color};">{shortf_branch[key]}</span> Students CGPA Ranking 2027'
                elif year_choosed == '2026':
                    flname = f'26_{key}_ranked_results.csv'
                    title_help = f'<span style="color: {color};">{shortf_branch[key]}</span> Students CGPA Ranking 2026'

rt.write(f"""
<h3 style="
text-align: center;
align-items: center;
">{title_help}</h3>
""",
         unsafe_allow_html=True)

df = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{flname}', dtype=str, index_col=None).fillna("")

dataspace = rt.empty()
dataspace.dataframe(df, hide_index=True, height=900, use_container_width=True)

# Filter the dataframe using masks !!!!!!!!! GOTT THIS FROM INTERNET! PLEASE LEARN PANDAS TO UNDERSTAND THIS
m1 = df["NAME"].str.contains(text_search.upper())
m2 = df["ROLL NO."].str.contains(text_search.upper())
df_search = df[m1 | m2]

# Show the results, if you have a text_search
if text_search:

    # IF USER HAS PUTTEN 2K/2k IN THE ROLL NUMBER, REMOVING THAT CAUSE, OUR DATA DOES NOT CONTAIN THAT
    if '2k' in text_search or '2K' in text_search:
        text_search = text_search.replace('2k', '').replace('2K', '').strip()

    # DEALING WITH USER PUTTEN ROLL NO. 23/EP/12  AND  23/EP/01
    if len(text_search) == 8:
        text_search = text_search[0:6] + '0' + text_search[6:]

    dataspace.dataframe(df_search, hide_index=True, height=525, use_container_width=True)