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




leftsec , rightsec, _ = st.columns([1.5,1,0.5])

with leftsec:

    st.write(f"""
                <h5 style="
                text-align: center;
                align-items: center;
                "><span style="color: {color};"></span>Enter How Many subjects do you have? :</h5>
                """,
             unsafe_allow_html=True)

    _, mm, _ = st.columns([0.35,1,0.35])
    with mm:
        nofs = st.number_input("", value=6, key='nofs', label_visibility='hidden', max_value=12, min_value=0)
        st.markdown("######")
        subbut = st.button('CALCULATE YOUR SGPA ACCORDING TO THESE GRADES:')

        if subbut:
            try:
                nofs = st.session_state.nofs
                total, crdtotal = 0, 0

                for i in range(nofs):
                    total += float(int(st.session_state.crList[i]) * (int(grdpoint[st.session_state.grdList[i]])))
                    crdtotal += float(st.session_state.crList[i])

                st.markdown('---')

                st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        padding-bottom: 0px;
                        border-bottom-width: 0px;
                        ">Predicted SGPA: <span style="color: {color};">{float(total / crdtotal)}</span></h3>
                        """,
                         unsafe_allow_html=True)

                st.markdown('---')

            except:
                st.warning('PLEASE ENTER VALID INFORMAION! ')

with rightsec:

    if nofs:
        st.session_state.crList = []
        st.session_state.grdList = []

        try:
            num = ([4]*(int(nofs)-1)) + [2,2]

            for i in range(int(nofs)+1):
                sec1, sec2, sec3 = st.columns([1.2, 0.95, 0.95])
                with sec1:
                    if i==0:
                        pass
                    else:
                        st.write(f"""
                            <h5 style="
                            padding-top: 35px;
                            color: #9DB4C0;
                            ">SUBJECT {i} -</h5>
                            """,
                    unsafe_allow_html=True)
                with sec2:

                    if i==0:
                        pass
                    else:
                        crd = st.number_input("CREDITS:", key=f'cr{i}', placeholder='Credits:', min_value=0, step=1, value=num[i])
                        st.session_state.crList.append(crd)

                with sec3:

                    if i==0:
                        pass
                    else:
                        grd = st.selectbox('GRADE: ', ['O', 'A+', 'A', 'B+', 'B', 'C','P' ,'F'], key=f'grd{i}', index=0)
                        st.session_state.grdList.append(grd)


        except:
            st.warning('ERROR OCCURED ENTER VALID IMFORMATION! ')