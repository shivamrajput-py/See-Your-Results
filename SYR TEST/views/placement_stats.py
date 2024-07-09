
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
        fl.write(f"""USER AT {datetime.datetime.now()} CLICKED "PLACEMENTS" (VIEW COUNTED)\n""")
        fl.flush()


#____________ 2023 PLACEMENTTS

st.write(f"""
        <h6 style="
        text-align: center;
        align-items: center;
        font-size: 13px;
        ">Be on Desktop mode to see the graphs properly!</h6>
        """,
         unsafe_allow_html=True)


st.write(f"""
    <h2 style="
    text-align: center;
    align-items: center;
    ">OVERALL <span style="color: {color};">2023</span> PLACEMENT STATS:</h2>
    """,
 unsafe_allow_html=True)

data23 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package23.csv').dropna()

df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'EC', 'EP', 'EN', 'IT', 'MC', 'ME', 'AE', 'CH', 'PE', 'SE'],
    'Avg CTC (in LPA)': data23['Avg CTC (in LPA)'].values
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

r,l = st.columns([1, 1])
_, m, _ = st.columns([0.3,1,0.3])

with r: st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2023', text_auto='').update_layout({'dragmode':False}), use_container_width=True,config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']})

data23 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package23.csv').dropna()

df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
    'Max CTC (in LPA)': data23['Max CTC (in LPA)'].values
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with l: st.plotly_chart(px.bar(df,  title='Highest Package from Every Branch in 2023', text_auto='').update_layout({'dragmode':False}), use_container_width=True,config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']})

data23 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv').dropna()
placed_Data = []
for val in data23['Placed (%)'].values: placed_Data.append(float(str(val).replace('%', '')))

df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE', 'OVERALL'],
    'Placed (%)': placed_Data
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with m: st.plotly_chart(px.bar(df, title='Percentage Of Students placed from every Branch in 2023',text_auto='', range_y=[0,100]).update_layout({'dragmode':False}), use_container_width=True,config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']})


#____________________ 2022 PALCEMENTS

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""<br>""", unsafe_allow_html=True)

st.write(f"""
        <h2 style="
        text-align: center;
        align-items: center;
        ">OVERALL <span style="color: {color};">2022</span> PLACEMENT STATS:</h2>
        """,
         unsafe_allow_html=True)

r1, l1 = st.columns([1,1])
_, m1, _ = st.columns([0.3, 1, 0.3])

data22 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package22.csv').dropna()
df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
    'Avg CTC (in LPA)': data22['Avg CTC (in LPA)'].values
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with r1: st.plotly_chart(px.bar(df,  title='Average Package of Every Branch in 2022', text_auto='').update_layout({'dragmode':False}), use_container_width=True,config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']})

data22 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package22.csv').dropna()

df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
    'Max CTC (in LPA)': data22['Max CTC (in LPA)'].values
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with l1: st.plotly_chart(px.bar(df,  title='Highest Package from Every Branch in 2022', text_auto='').update_layout({'dragmode':False}),config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']}, use_container_width=True)

data22 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed22.csv').dropna()
placed_Data = []
for val in data22['Placed (%)'].values: placed_Data.append(float(str(val).replace('%', '')))
df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE', 'OVERALL'],
    'Placed (%)': placed_Data
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with m1: st.plotly_chart(px.bar(df,  title='Percentage Of Students placed from every Branch in 2022' ,range_y=[0, 100], text_auto='').update_layout({'dragmode':False}),config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']}, use_container_width=True)

#____________________ 2021 PLACEMENTS

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""<br>""", unsafe_allow_html=True)


st.write(f"""
        <h2 style="
        text-align: center;
        align-items: center;
        ">OVERALL <span style="color: {color};">2021</span> PLACEMENT STATS:</h2>
        """,
         unsafe_allow_html=True)



r2, l2 = st.columns([1,1])
_, m2, _ = st.columns([0.3, 1, 0.3])

data21 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package21.csv').dropna()

df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
    'Avg CTC (in LPA)': data21['Avg CTC (in LPA)'].values
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with r2: st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2021', text_auto='').update_layout({'dragmode':False}),config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']}, use_container_width=True)

data21 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package21.csv').dropna()

df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
    'Max CTC (in LPA)': data21['Max CTC (in LPA)'].values
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with l2: st.plotly_chart(px.bar(df, title='Highest Package from Every Branch in 2021', text_auto='').update_layout({'dragmode':False}),config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']}, use_container_width=True)

data21 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv').dropna()
placed_Data = []
for val in data21['Placed (%)'].values: placed_Data.append(float(str(val).replace('%', '')))
df = pd.DataFrame({
    'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE', 'OVERALL'],
    'Placed (%)': placed_Data
})

df.reset_index(drop=True)
df.set_index('Branch', inplace=True)

with m2: st.plotly_chart(px.bar(df,title= 'Percentage of Student placed from every Branch in 2021',  range_y=[0, 100], text_auto='').update_layout({'dragmode':False}),config={"modeBarButtonsToRemove": [ 'lasso2d', 'select2d']} ,use_container_width=True)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("---")
