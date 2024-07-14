import csv
import time
import streamlit as st
import json
import pandas as pd
import plotly_express as px
from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
from MainConstant import *
from streamlit_extras.let_it_rain import rain
import os
import datetime
import statistics

import warnings
warnings.filterwarnings('ignore')

# color_discrete_sequence=['#50aef6']

st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='DTU ANALYSIS', page_icon='🎓')

color = '#1F51FF' # USE FOR HIGHLIGHTING A SPECIFIC WORD
other= False

with open('style.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# FOR LOADING THE ANIMATION !!
@st.experimental_fragment
def load_lottieurl(isjson: bool, url_or_path: str):
    if isjson:
        with open(url_or_path, 'r') as fl:
            return json.loads(fl.read())
    else:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


#SGPA CALCULATOR FUNCTION!!!!!---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# SGPA CALCULATOR FUNCTION WITH A EXPERIMENTAL DIALOG
@st.experimental_dialog("SGPA CALCULATOR", width="small")
def sgpacal():
    st.write(f"""
                <h4 style="
                text-align: center;
                align-items: center;
                padding-bottom: 0px;
                "><span style="color: {color};"></span>Enter How Many subjects do you have? :</h4>
                """,
             unsafe_allow_html=True)

    with st.columns([0.35, 1, 0.35])[1]:
        nofs = st.number_input("", value=6, key='nofs', label_visibility='hidden', max_value=12, min_value=0)
        st.markdown("######")
        subbut = st.button('CALCULATE YOUR SGPA ACCORDING TO THESE GRADES:')

        if subbut:
            # try:

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

            # except:
            #     st.warning('PLEASE ENTER VALID INFORMAION! ')

    if nofs:
        st.session_state.crList = []
        st.session_state.grdList = []


        num = ([4] * (int(nofs) - 1)) + [2, 2]

        for i in range(int(nofs) + 1):
            sec1, sec2 = st.columns([1,1], vertical_alignment='center')

            with sec1:
                if i == 0: pass
                else:
                    crd = st.number_input(f"Subject {i} Credits:", placeholder='Credits:', min_value=0, step=1,value=num[i])
                    st.session_state.crList.append(crd)

            with sec2:
                if i == 0: pass
                else:
                    grd = st.selectbox(f'Subject {i} Grade:', ['O', 'A+', 'A', 'B+', 'B', 'C', 'P', 'F'], index=0)
                    st.session_state.grdList.append(grd)

            st.markdown("---")


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.experimental_fragment
def find(SUBC: str, TYPE: str, sendsorted=True) -> dict:

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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.experimental_fragment
def ranksNresults_menu():
    lf, rt = st.columns([0.5, 3])

    with lf:
        st.markdown('<br>', unsafe_allow_html=True)

        year_choosed = st.selectbox('Choose Year', ['2027', '2026'], index=0)
        if year_choosed == '2026':
            shortf_branch = shortf_branch26
        elif year_choosed == '2027':
            shortf_branch = shortf_branch27

        brnch_choosed = st.selectbox('Choose Branch', ['Cumulative'] + list(shortf_branch.values()), index=0)

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

#PLACEMENT STATS MENU FUNCTION!!!---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.experimental_fragment
def placement_menu():
    # ----------------------------- 2023 PALCEMENTS ----------------------------------------------

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

    r, l = st.columns([1, 1])
    _, m, _ = st.columns([0.3, 1, 0.3])

    with r:
        st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2023', text_auto='').update_layout(
            {'dragmode': False}), use_container_width=True, config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']})

    data23 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package23.csv').dropna()

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Max CTC (in LPA)': data23['Max CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with l:
        st.plotly_chart(px.bar(df, title='Highest Package from Every Branch in 2023', text_auto='').update_layout(
            {'dragmode': False}), use_container_width=True, config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']})

    data23 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv').dropna()
    placed_Data = []
    for val in data23['Placed (%)'].values: placed_Data.append(float(str(val).replace('%', '')))

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE', 'OVERALL'],
        'Placed (%)': placed_Data
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with m:
        st.plotly_chart(px.bar(df, title='Percentage Of Students placed from every Branch in 2023', text_auto='',
                               range_y=[0, 100]).update_layout({'dragmode': False}), use_container_width=True,
                        config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']})

    # ----------------------------- 2022 PALCEMENTS ----------------------------------------------

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

    r1, l1 = st.columns([1, 1])
    _, m1, _ = st.columns([0.3, 1, 0.3])

    data22 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package22.csv').dropna()
    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Avg CTC (in LPA)': data22['Avg CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with r1:
        st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2022', text_auto='').update_layout(
            {'dragmode': False}), use_container_width=True, config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']})

    data22 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package22.csv').dropna()

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Max CTC (in LPA)': data22['Max CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with l1:
        st.plotly_chart(px.bar(df, title='Highest Package from Every Branch in 2022', text_auto='').update_layout(
            {'dragmode': False}), config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}, use_container_width=True)

    data22 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed22.csv').dropna()
    placed_Data = []
    for val in data22['Placed (%)'].values: placed_Data.append(float(str(val).replace('%', '')))
    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE', 'OVERALL'],
        'Placed (%)': placed_Data
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with m1:
        st.plotly_chart(px.bar(df, title='Percentage Of Students placed from every Branch in 2022', range_y=[0, 100],
                               text_auto='').update_layout({'dragmode': False}),
                        config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}, use_container_width=True)

    # ----------------------------- 2021 PALCEMENTS ----------------------------------------------

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

    r2, l2 = st.columns([1, 1])
    _, m2, _ = st.columns([0.3, 1, 0.3])

    data21 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package21.csv').dropna()

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Avg CTC (in LPA)': data21['Avg CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with r2:
        st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2021', text_auto='').update_layout(
            {'dragmode': False}), config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}, use_container_width=True)

    data21 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package21.csv').dropna()

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Max CTC (in LPA)': data21['Max CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with l2:
        st.plotly_chart(px.bar(df, title='Highest Package from Every Branch in 2021', text_auto='').update_layout(
            {'dragmode': False}), config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}, use_container_width=True)

    data21 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv').dropna()
    placed_Data = []
    for val in data21['Placed (%)'].values: placed_Data.append(float(str(val).replace('%', '')))
    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE', 'OVERALL'],
        'Placed (%)': placed_Data
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with m2:
        st.plotly_chart(px.bar(df, title='Percentage of Student placed from every Branch in 2021', range_y=[0, 100],
                               text_auto='').update_layout({'dragmode': False}),
                        config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}, use_container_width=True)

    st.markdown("""<br>""", unsafe_allow_html=True)
    st.markdown("---")


#STUDY RESORUCES MATERIALS MENU FUNCTION---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.experimental_fragment
def studyResources_menu():
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

    with s1:
        RESOURCE_BRNCH = st.selectbox("CHOOSE BRANCH: ", shortf_branch27.values(), placeholder='BRANCH')

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
                RESOURCE_SEM = st.selectbox("CHOOSE SEMESTER: ", DATA[0][RESOURCE_BRNCH].keys(),
                                            placeholder='SEMEMSTER', index=1)
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
                        RESOURCE_TYPE = st.selectbox("CHOOSE TYPE: ",
                                                     ['PYQ', 'NOTES', 'PLAYLISTS', 'ASSIGNMENTS', 'BOOKS'], index=0,
                                                     placeholder='TYPE')
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


# ABOUT SECTIOO OF MAIN MENU FUNCTION STARTS HERE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.experimental_fragment

def aboutsection_menu():
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
            width=530,)

        with l_:
            st.write(f"""
                    <h4>Hey, SHIVAM Here<br>Engineering Physics 2027</h4>
                    """,
                     unsafe_allow_html=True)

        with m_:
            st.markdown('######')
            st.markdown(
                '''<a class="social1_" href="https://www.instagram.com/shivammm20_/"><button class="button-62" type="button">INSTA</button>''',
                unsafe_allow_html=True)

        with r_:
            st.markdown('######')
            st.markdown(
                '''<a class="social1_" href="https://www.linkedin.com/in/shivam-rajput-3928a328a/"><button class="button-18" type="button">LINKEDIN</button>''',
                unsafe_allow_html=True)

    with lc:
        st.write(f"""
            <h1 class="nametit">Your Education<br>Dashboard<br><span class="nametitm">DTU RESULTS</span></h1>
                    <br>""", unsafe_allow_html=True)

        st.markdown('<br>', unsafe_allow_html=True)

        sgpcalButton = st.button("WANNA CALCULATE YOUR SGPA ?")
        if sgpcalButton:
            sgpacal()
            st.rerun()

        st.write(f"""
                <h3 class="about">MORE <span style="color: #1F51FF;">FEATURES</span> TO COME, IN FURTHER UPDATES</h3>
                <h6 class="about">- 2nd Sem results ? YES I WILL UPDATE, After Results, ASAP!</h6>
                <h6 class="about">- What about 2025 Results etc? YES I am going to add them too, it will take time. </h6>
                <h6 class="about">- Other than this, Suggest me what more should i add ?</h6>
                """,
                 unsafe_allow_html=True)

        st.markdown('<br><br><br>', unsafe_allow_html=True)

    # st.warning("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF'S, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR YOU FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE CONTACT ME, I WILL SOLVE IT ASAP!")


# MAIN EXECUTION CODE STARTS FROM HERE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# MAIN MENU COLUMNS FOR LOGO ANIMATION AND REAL MAIN MENU
mainmenu_left, mainmenu_middle,_ = st.columns(spec=[0.8,3,0.8])

with mainmenu_left:
    pass
    # st.image("") CAN PUT YOUR LOGO HERE !!!

    st_lottie(
        load_lottieurl(True, "./animation/hat_w_books.json"),
        speed=0.7,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=80,
        width=80,
        key=None,
    )

# FOR MAKING THE MENU TRANSPARENT!! #0e1117


with mainmenu_middle:
    selected = option_menu(menu_title=None, options= ['PROFILE', 'RANKS','PLACEMENTS','STUDY' ,'ABOUT'],
                           default_index=0,
                           icons=['person-vcard', 'bar-chart-line','clipboard-data','journals','info-square'],
                           menu_icon='cast',
                           orientation='horizontal',
                           styles={
                               "container": {"padding": "1!important", "background-color": "#262730"},
                               "icon": {"color": "white", "font-size": "14px"},
                               "nav-link": {"font-size": "14px", "text-align": "center", "margin": "2px"},
                               "nav-link-selected": {"background-color": "#05acff", "font-weight": "800"}}
                           )

#--------------------------------------------------MENU: [STUDENT PROFILE] STARTED-----------------------------------------------------------------------------------------------------------------------

if selected=='PROFILE':

    _,search_middle, _ = st.columns([0.5,1,0.5])

    Mtitle = search_middle.empty()
    Mtitle.write(f"""
    <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2027</h2>
    """,
    unsafe_allow_html=True)

    _, description, _ = st.columns([1,3,1])
    descripE = description.empty()
    with descripE: st.markdown("""
    <h5 style="text-align: center; align-items: center;">Enter your roll number to access a comprehensive summary of your semester grades and academic performance. A detailed report will be generated upon entry.</h2>
    """, unsafe_allow_html=True)

    _,filt1,filt2, _ = st.columns([2.2,1,1,2.2])

    with filt1:
        st.markdown('<br>', unsafe_allow_html=True)
        year_choosed = st.selectbox("Choose Year", ['2027' ,'2026'], index=0)
    with filt2:
        st.markdown('<br>', unsafe_allow_html=True)
        result_search_box = st.text_input("Enter Your Roll Number", value='', placeholder='__/__/___')

    if year_choosed=='2026':
        Mtitle.write(f"""
            <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2026</h2>
            """,unsafe_allow_html=True)




#-----------------------------SPECIAL ADDITION IN THE WEBSITE, KIRTI--------------------------------------------------------------------------------------------------------

    if 'best gc' in result_search_box.lower() or 'sexy gc' in result_search_box.lower() or 'w gc'  in result_search_box.lower():
        descripE.empty()
        other = True
        st.header("OHH YOU ASKED ABOUT THE BEST GC ?")
        st.subheader("Well lemme tell you....")

        st.write(f"""
                                    <h6 style="text-align: center; align-items: center;"><span style="color: {color};"></span>Keep Scrolling down as the page loads more lines by itself :)</h6>
                                    """, unsafe_allow_html=True)

        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

        st.write(f"""
                            <h3 style="text-align: center; align-items: center;"><span style="color: {color};"></span>THE BEST GC AWARD GOES TO !!!???</h3>
                            """, unsafe_allow_html=True)

        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        time.sleep(2)

        st.write(f"""
                                    <h1 style="text-align: center; align-items: center;"><span style="color: {color};">THE GROUP SEXTING</span></h1>
                                    """, unsafe_allow_html=True)

        time.sleep(4)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.write(f"""
                    <h3 style="text-align: center; align-items: center;">REAL BKCHOD FUN<span style="color: {color};"> GC </span> HAI! ISME VO VIBE TO HAI! FR.</h3>
                    """, unsafe_allow_html=True)

        time.sleep(4.5)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.columns([0.3,1,0.3])[1].write(f"""
                            <h4 style="text-align: center; align-items: center;">I'VE NAMES OF SOME SPECIFIC MEMBERS JOKI MUJHE JADA <span style="color: {color};"> PASAND AAYE  </span>BUT WILL NOT TELL THE NAMES, LAFDE HOJAYENGE GC MAI YE SAB ACHAA NHI LAGTA  😔</h4>
                            """, unsafe_allow_html=True)

        time.sleep(10)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.write(f"""
                                    <h3 style="text-align: center; align-items: center;">VESE TO MUJHE JOIN HEE KARE 1 DIN HUA H 🤣<span style="color: {color};"></span></h3>
                                    """, unsafe_allow_html=True)

        time.sleep(4)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.write(f"""
                                            <h4 style="text-align: center; align-items: center;">And Yeah credits to all the <span style="color: {color};">ADMINS</span> and Members</h4>
                                            """, unsafe_allow_html=True)

        time.sleep(4)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.columns([0.3,1,0.3])[1].write(f"""
                                                    <h5 style="text-align: center; align-items: center;">ALSO Y'ALL MUST BE THINKING SHIVAM NIGGA WHY SO SWEET? VOTO KYA HAI SIRF <span style="color: {color};"> 1-2 DIN HUA H </span>ISLIYE I ONLY GOT TARIFS 1 WEEK BAAD SAME YAHIN AANA BHT KUCH ACHAA LIKHA HOGA 🥰</h5>
                                                    """, unsafe_allow_html=True)

        time.sleep(10)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

        st.columns([0.3,1,0.3])[1].write(f"""
                                                            <h4 style="text-align: center; align-items: center;">SEE THIS IS WHERE BAKCHODI AND ROTTEN MIND TAKES YOU! <span style="color: {color};">LIKE KON</span> HEE EK WEB PAGE BANATA HOGA AISA JUST FOR THE FUN! ITS ME 😭</h4>
                                                            """, unsafe_allow_html=True)

        time.sleep(7)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

        st.write(f"""
                                                                    <h4 style="text-align: center; align-items: center;">OKI END OF THE PAGE MOST PROBABLY <span style="color: {color};"></span> AB EMOJI RAIN HOGA HEHEHEHEHE</h4>
                                                                    """, unsafe_allow_html=True)

        time.sleep(7)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

        st.write(f"""
                                                                            <h4 style="text-align: center; align-items: center;">THE EMOJIS ARE THE EMOTIONS WE FEEL IN THIS GC IG<span style="color: {color};"></span> ALSO WINDOWS EMOJIS SUCKS!</h4>
                                                                            """, unsafe_allow_html=True)

        time.sleep(7)
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

        st.write(f"""
                                                                                    <h4 style="text-align: center; align-items: center;">Bhai REAL bkchodi type Rain karne wala hun pasand na aaye to reload krdena 😭😭🎀<span style="color: {color};"></span></h4>
                                                                                    """, unsafe_allow_html=True)



        time.sleep(4)

        emoji = ['💀', '😂','😭', '🎀','🤣', '🫦','🥵', '😤', '🖤', '💀','💦', '😂','😭', '🎀','🤣', '🫦','🥵', '😤', '🖤']
        for i in range(16):
            rain(
                emoji[i], falling_speed=0.8,
            )
            time.sleep(0.9)





    if result_search_box and '19012007' == result_search_box:
        descripE.empty()
        other = True
        st.subheader('IS KIRTI :pouting_cat: HERE ? WTF ARE YOU DOING HERE!')
        st.write("I actually don't know whether you are the kri-tikka ik or someone else?")
        st.write('Give me the right answer of the question written below:')
        kiritbox = st.text_input(label='kiritbox',label_visibility="hidden", value='', placeholder='What is that short name that you gave it to yourself, after that i started calling you by that name!')
        if kiritbox:
            if kiritbox == 'kirit' or kiritbox == 'Kirit' or kiritbox == 'KIRIT':
                st.warning("YOU ARE THE KRITIKA :smile_cat: I KNOW, I MEAN KIRIT BKL 🥰")
                kiriti = ['WELCOME TO','MY WEBSITE', 'MISS CERTIFIED', 'BIG W YAPPER', 'KRITIKA SINHA :smirk_cat:']
                for i in range(52):
                    st.markdown("""<br>""", unsafe_allow_html=True)
                    if (i==3):
                        k, _, _, _, _ = st.columns(5)
                        k.markdown(f'# {kiriti[0]}')
                        k.markdown('<h6>bhaag ja bhen ki lauri</h6>', unsafe_allow_html=True)
                    elif (i==15):
                        _, k, _, _, _ = st.columns(5)
                        k.markdown(f'# {kiriti[1]}')
                        k.markdown('<h6>Consider Yourself Special bich</h6>', unsafe_allow_html=True)

                    elif (i==27):
                        _, _, k, _, _ = st.columns(5)
                        k.markdown(f'# {kiriti[2]}')
                        k.markdown('<h6>not your average Biharan</h6>', unsafe_allow_html=True)

                    elif (i==39):
                        _, _, _, k, _ = st.columns(5)
                        k.markdown(f'# {kiriti[3]}')
                        k.markdown('<h6>the W in your name stands for WIN</h6>', unsafe_allow_html=True)

                    elif (i==51):
                        _, _, _, _, k = st.columns(5)
                        k.markdown(f'# {kiriti[4]}')
                        k.markdown('<h6 style="color: pink;">Kirti THE gori niggru, fr <3</h6>', unsafe_allow_html=True)

                kiriti = ['YOU ARE REALLY', 'A PERFECT W', 'A 10/10 BADDIE', 'PRETTY BICH',
                          'MY SALI, LITERALLY THE BEST SALI 🎀']


                for i in range(54):
                    st.markdown("""<br>""", unsafe_allow_html=True)

                    if (i==6):
                        _, _, _, _, k = st.columns(5)
                        k.markdown(f'## {kiriti[0]}')
                        k.markdown('<h6>A Magical god-crafted SHIT, yes</h6>', unsafe_allow_html=True)

                    if (i==17):
                        _, _, _, k, _ = st.columns(5)
                        k.markdown(f'## {kiriti[1]}')
                        k.markdown('<h6>W = Womp Womp nigggaahhhoee</h6>', unsafe_allow_html=True)

                    if (i==29):
                        _, _, k, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[2]}')
                        k.markdown('<h6>you will surely bad-DIE</h6>', unsafe_allow_html=True)

                    if (i==41):
                        _, k, _, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[3]}')
                        k.markdown("<h6>It ain't a lie tho, everything is</h6>", unsafe_allow_html=True)

                    if (i==53):
                        k, _, _, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[4]}')
                        k.markdown("""<h6 style="color: pink;">Kya expect kra another reply, NO, it is acutally true ehehehe <3</h6>""", unsafe_allow_html=True)

                st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
                lef, _ , rig = st.columns([1.6,2, 1.7])

                with lef:

                    st.markdown('''<h1 style="color: #D27D2D;">SO, KIRTI</h1>''', unsafe_allow_html=True)
                    st.markdown("""<br>""", unsafe_allow_html=True)
                    st.markdown('''<h6 style="color: white;">How you doing? All well i hope so, How's my rishika, I hope she is well too,I am writing this considering
the future aspect too! KEEP STUDYING KIRTI, Cause you know what, nothing remains in life except your work so yayy,
simple Jiju advice. Also Improve your choice in dating men ,It Sucks! Best wishes for Your Upcoming CA foundation,
I hope you clear it with good marks and come to delhi soon, tbh bit excited bout it! so kirit gora niggru tbh idk
what to say more, i suck at writing shit like this. Haan, Thank you for being a good supportive sali,
for giving me gifts suggestions, Thank you for being TOO much nice to me, its always fun to fight w ya, tbh my vocab,
arguements skills, homour got improved somehow by daily this fighting bkchodi with ya. I Like those silly convo between US Dumbfucks, That Vibe>>></h5>''',
                        unsafe_allow_html=True)

                with rig:
                    st.markdown('''<h1 style="color: #D27D2D;">~KRITIKA SINHA~</h1>''', unsafe_allow_html=True)
                    st.markdown("""<br>""", unsafe_allow_html=True)
                    st.write('- The N in your Name Stands for How much NERD You are')
                    st.write('- The T in your Name Stands for How much TRASH you are')
                    st.write('- The M in your Name Stands for How much Mardana you are')
                    st.write('- The A in your Name Stands for How Amazing You are')
                    st.write('- The R in your Name Stands for How Rare You are')
                    st.write('- The B in your Name Stands for that BIG Dick You have')
                    st.write('- The S in your Name Stands for How Smart & Sweet You are')
                    st.write('- The H in your Name Stands for that Sexy Humour you got')


                kiriti = ['KRI-TIKKA', 'WHITE NIGGAHH', 'YOU ARE TOOO MUCHHHH', 'NERD, MARD WITH BIG D',
                          'SALI JII, BUS JAIYE AB AAP']
                for i in range(46):
                    st.markdown("""<br>""", unsafe_allow_html=True)
                    if (i == 3):
                        k, _, _, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[0]}')
                        k.markdown('<h6>urff DeepFriedChicken 💅🏻</h6>', unsafe_allow_html=True)

                    if (i == 13):
                        _, k, _, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[1]}')
                        k.markdown('<h6>Silly dumb nigga, BUT<br>YOUR MUSIC TASTE>>>🙇🏻</h6>', unsafe_allow_html=True)

                    if (i == 23):
                        _, _, k, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[2]}')
                        k.markdown('<h6>Hot to handle? naah! Skinny(joks)</h6>', unsafe_allow_html=True)

                    if (i == 33):
                        _, _, _, k, _ = st.columns(5)
                        k.markdown(f'## {kiriti[3]}')
                        k.markdown("<h6>irl, 5'3 pookie 🐥, will get<br>scared of Cock-roach</h6>", unsafe_allow_html=True)

                    if (i == 43):
                        _, _, _, _, k = st.columns(5)
                        k.markdown(f'## {kiriti[4]}')
                        k.markdown('<h6 style="color: #ffc1cc;">REALLY A 10/10 W SALI.</h6>', unsafe_allow_html=True)
                        k.markdown("""<h6 style="color: #ffc1cc;">MERI SALI ✔️ MY SISTER IN LAW ❌</h6>""",unsafe_allow_html=True)
                        k.markdown("""<h6 style="color: #ffc1cc;">BYEEEE, ITNA HEE THA,<br>KEEP REVISITING KIRTI 🤍</h6>""", unsafe_allow_html=True)


                st.markdown('<br><br><br><br><br><br><br>', unsafe_allow_html=True)


                st.markdown("""<h1 style="color: babypink; text-align: center;">AAB JAA NAA BHEN KI LAURI, HOGYA NAA</h1>""", unsafe_allow_html=True)

            else:
                st.warning("EITHER YOU ARE NOT KIRTI OR YOU ARE, BUT YOU DON'T KNOW THE ANSWER ! L KIRTI")

#--------------------------ENDING OF SPECIAL ADDITION IN THE WEBSITE-----------------------------------------------------------------------------------------------------

    if year_choosed=='2027' and result_search_box:
        descripE.empty()

        # IF USER HAS PUTTEN 2K/2k IN THE ROLL NUMBER, REMOVING THAT CAUSE, OUR DATA DOES NOT CONTAIN THAT
        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box= result_search_box.replace('2k', '').replace('2K', '').strip()

        # DEALING WITH USER PUTTEN ROLL NO. 23/EP/12  AND  23/EP/01
        if len(result_search_box)==8:
            result_search_box  = result_search_box[0:6] + '0' + result_search_box[6:]

        # AFTER SEM2 RESULTS THERE GONNA BE JUST 1 FILE 27UNI_ranked_results.csv !!!!!
        jsondf = pd.read_json("./Extracting_Result_Data/extracted_data_json/uniwise_ranked_results.json")
        m1 = jsondf['rolln'].str.contains(result_search_box.upper())
        df_final = jsondf[m1]

        if (len(df_final)>1 or len(df_final)<1) and not other:
            st.markdown('<br><br><br>', unsafe_allow_html=True)
            st.error("No student was found with the provided roll number. Please verify the roll number and try again. If you believe this is a mistake, please contact the Project Maintainer.")
            st.error("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE SHARE (GO TO ABOUT SECTION), I WILL SOLVE IT ASAP!")

        elif len(df_final)==1:

            stud_branch = str(df_final['rolln'].values[0])[3:5]
            stud_sem = 1 # A VERY UNNECESSARY VARIABLE, SEM2 UPDATE THIS GONNA BE REMOVED
            stud_branch_rank = None
            stud_university_rank = df_final['rank'].values[0]

            with open('./Extracting_Result_Data/extracted_data_json/branchwise_ranked_results.json', 'r') as fl:
                dt = json.loads(fl.read())
                for sd in dt[str(stud_sem)+'_'+str(stud_branch)]:
                    if sd['rolln'] == df_final['rolln'].values[0]:
                        stud_branch_rank = sd['rank']
                brnch_nofs = len(dt[str(stud_sem)+'_'+str(stud_branch)])

            stud_brnch_percentile = round(float(((brnch_nofs-stud_branch_rank)/brnch_nofs)*100), 4)
            stud_percentile = round(float(((2589.0-stud_university_rank)/2589.0)*100), 4)

            # MENU1: FIRST MAIN DIV WITH 3 COLUMNS ---------------------------------------------
            l_sec1 ,m_sec1,  r_sec1 = st.columns([1.5,2,1])

            with l_sec1:

                st.markdown('<br><br>', unsafe_allow_html=True)

                st.write(f"""
                <h2 class="nametit__">HELLO, {df_final['name'].values[0]}</h2>
                <h5>{stud_branch}, {shortf_branch27[stud_branch]}, B. TECH</h5>
                <h5>{df_final['rolln'].values[0]}</h5>
                <h5>1st SEMESTER: </h5>
                """,
                unsafe_allow_html=True)

                l1,l2 = st.columns(2)
                l1.metric(label="Credits Completed" , value=df_final['credits'].values[0] )
                l2.metric(label="Cumulative CGPA" , value=+df_final['sgpa'].values[0])

            with m_sec1:

                st.markdown('<br><br><br>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                | Credits Completed | Cumulative CGPA | University Rank | Branch Rank |
                | :------------ | :--------------- | :---------------| :---------------|
                | {df_final['credits'].values[0]}<br> | {df_final['sgpa'].values[0]}<br> | {stud_university_rank}<br> | {stud_branch_rank}<br> |
                """,
                    unsafe_allow_html=True,
                )
                st.markdown('<br><br>', unsafe_allow_html=True)

                if stud_percentile>50:
                    st.write(f"""
                        <h5>You Are in TOP <span style="color: #87CEFA;">{round(100-stud_percentile, 4)}%</span> Students of University!</h5>
                        """, unsafe_allow_html=True)
                else:
                    st.write(f"""
                        <h5>You Performed better than <span style="color: #87CEFA;">{round(stud_percentile, 4)}%</span> Students of University!</h5>
                        """, unsafe_allow_html=True)

                st.markdown('<br>', unsafe_allow_html=True)

                if stud_brnch_percentile>50:
                    st.write(f"""
                        <h5>You Are in TOP <span style="color: #87CEFA;">{round(100-stud_brnch_percentile, 4)}%</span> Students of Your Branch!</h5>
                        """, unsafe_allow_html=True)
                else:
                    st.write(f"""
                        <h5>You Performed better than <span style="color: #87CEFA;">{round(stud_brnch_percentile, 4)}%</span> Students of your Branch</h5>
                        """, unsafe_allow_html=True)

            with r_sec1:

                st.markdown('<br><br>', unsafe_allow_html=True)

                st_lottie(
                    load_lottieurl(True, "./animation/flying_student.json"),
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="low",  # medium ; high
                    height=None,
                    width=None,
                    key=None,
                )

            st.markdown('---')

            # MENU1: SECOND MAIN DIV WITH 2 COLUMNS ---------------------------------------------

            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{stud_branch}'27</span> and Your CGPA Distribution Stats:</h3>
                        """, unsafe_allow_html=True)

            _, l_sec2, _,r_sec2, _ = st.columns([0.9,3.1,1,3.1,0.5])

            with l_sec2:

                brnch_cg = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/cg_analysis.csv', index_col=None)

                for brnach_srn, branch_name in enumerate(brnch_cg['BRANCH'].values):
                    if stud_branch in branch_name: i=brnach_srn

                brnch_cg['Your'][i] = df_final['sgpa'].values[0]

                df = pd.DataFrame({
                    'Branch Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [brnch_cg['Highest'].values[i],brnch_cg['Average'].values[i],brnch_cg['Your'].values[i],brnch_cg['Max Appeared'].values[i],brnch_cg['Lowest'].values[i]]})

                df.reset_index(drop=True)
                df.set_index('Branch Stats', inplace=True)

                st.plotly_chart(px.bar(df,title=f"{stud_branch}'27 CGPA Distribution", range_y=[0,10], text_auto='', width=430).update_layout({'dragmode':False}), config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'zoomOut2d', 'select2d']})

            with r_sec2:

                uni_cg = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/cg_analysis.csv', index_col=None)
                brnch_cg['Your'][0] = df_final['sgpa'].values[0]

                df = pd.DataFrame({
                    'University Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [brnch_cg['Highest'].values[0], brnch_cg['Average'].values[0], brnch_cg['Your'].values[0],brnch_cg['Max Appeared'].values[0], brnch_cg['Lowest'].values[0]]})

                df.reset_index(drop=True)
                df.set_index('University Stats', inplace=True)

                st.plotly_chart(px.bar(df, title=f'University CGPA Distribution', range_y=[0,10] ,text_auto='', width=430).update_layout({'dragmode':False}), config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'zoomOut2d', 'select2d']})


            #MENU1: THIRD MAIN DIV WITH 1 COLUMNS--------------------------------------------------------------------------------------------------

            st.markdown('---')

            df = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/1_{stud_branch}_ranked_results.csv', dtype=str, index_col=None).fillna("")

            st.write(f"""
            <h3 style="
            text-align: center;
            align-items: center;
            ">Your Branch <span style="color: {color};">{stud_branch}'27</span> Students Rankings: </h3>
            """,unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            _,mm,_ = st.columns([1,4,1])
            with mm:
                ranklist = st.empty()
                ranklist.dataframe(df, hide_index=True, use_container_width=True, height= 425)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('---')
            #MENU1: FOURTH MAIN DIV WITH 3 COLUMNS --------------------------------------------------------------------------------------------------

            st.write(f"""
            <h3 style="
            text-align: center;
            align-items: center;
            ">Your Branch <span style="color: {color};">{shortf_branch27[stud_branch]}</span> Placement Stats:</h3>
            """,
            unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # AVERAGE PLACEMENTS

            # data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0] FOR ACCESING VALYE OF PLACEMENT DIRECTLY
            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                'AVERAGE PACKAGE': [
                    data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0],
                    data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0],
                    data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0]
                ]})


            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            avg_placement_barc = px.bar(df, title=f"Average Package Trend (IN LPA)", text_auto='').update_layout({'dragmode':False})

            # HIGHEST PLACEMENTS

            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                'HIGHEST PACKAGE': [
                    data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Max CTC (in LPA)'].values[0],
                    data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Max CTC (in LPA)'].values[0],
                    data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Max CTC (in LPA)'].values[0]
                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            max_placement_barc = px.bar(df, title=f"Highest Package Trend (IN LPA)", text_auto='').update_layout({'dragmode':False})

            # PERCENTAGE PLACED PLACEMENT

            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                '% STUDENT PLACED': [
                    float(data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%', '')),
                    float(data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%', '')),
                    float(data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%', ''))
                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            percent_placement_barc = px.bar(df, title=f"Percentage Of Student Placed", range_y=[0,100], text_auto='').update_layout({'dragmode':False})

            bar1, bar2, bar3 = st.columns(3)
            with bar1: st.plotly_chart(avg_placement_barc, use_container_width=True, config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d']})
            with bar2: st.plotly_chart(max_placement_barc, use_container_width=True, config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d']})
            with bar3: st.plotly_chart(percent_placement_barc, use_container_width=True, config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d']})

            st.markdown('---')


    elif year_choosed=='2026' and result_search_box:
        descripE.empty()

        # IF USER HAS PUTTEN 2K/2k IN THE ROLL NUMBER, REMOVING THAT CAUSE, OUR DATA DOES NOT CONTAIN THAT
        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box= result_search_box.replace('2k', '').replace('2K', '').strip()

        # DEALING WITH USER PUTTEN ROLL NO. 23/EP/12  AND  23/EP/01
        if len(result_search_box)==8:
            result_search_box  = result_search_box[0:6] + '0' + result_search_box[6:]

        data26std = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/26_UNI_ranked_results.csv')
        m1 = data26std['ROLL NO.'].str.contains(result_search_box.upper())
        df_final = data26std[m1]

        if (len(df_final)>1 or len(df_final)<1) and not other:
            st.markdown('<br><br><br>', unsafe_allow_html=True)
            st.error("No student was found with the provided roll number. Please verify the roll number and try again. If you believe this is a mistake, please contact the Project Maintainer.")
            st.error("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE SHARE (GO TO ABOUT SECTION), I WILL SOLVE IT ASAP!")

        elif len(df_final)==1:

            stud_branch = str(df_final['ROLL NO.'].values[0])[3:5]
            stud_cum_cgpa = df_final['Cumulative CGPA'].values[0]
            stud_branch_rank = None
            stud_university_rank = df_final['RANK'].values[0]

            # HAD TO FIND THE BRANCH RANK ALAG SE !
            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/26_{stud_branch}_ranked_results.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper())
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_brnch_percentile = round(float(((len(fl.values)-stud_branch_rank)/len(fl.values))*100), 4)
            stud_percentile = round(float(((2579.0 - stud_university_rank) / 2579.0) * 100), 4)

            l_c, m_c, r_c = st.columns([1.5, 2, 1])

            with l_c:

                st.markdown('<br><br>', unsafe_allow_html=True)

                st.write(f"""
                            <h2 class="nametit__">HELLO, {df_final['NAME'].values[0]}</h2>
                            <h5>{stud_branch}, {shortf_branch26[stud_branch]}, B. TECH</h5>
                            <h5>{df_final['ROLL NO.'].values[0]}</h5>
                            <h5>RESULTS:- </h5>
                            """,
                         unsafe_allow_html=True)

                l1, l2, l3  = st.columns(3)
                l1.metric(label="1ST SEM CG", value=df_final['SEM1'].values[0])
                l2.metric(label="2ND SEM CG", value=df_final['SEM2'].values[0], delta=round(float(df_final['SEM2'].values[0])-float(df_final['SEM1'].values[0]), 2))
                l3.metric(label="3RD SEM CG", value=df_final['SEM3'].values[0], delta=round(float(df_final['SEM3'].values[0])-float(df_final['SEM2'].values[0]), 2))

            with m_c:

                st.markdown('<br><br><br>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                            | Total Credits | Cumulative CGPA | University Rank | Branch Rank |
                            | :--------------- | :--------------- | :---------------| :---------------|
                            | Yet to Add | {df_final['Cumulative CGPA'].values[0]}<br> | {stud_university_rank}<br> | {stud_branch_rank}<br> |
                            """,
                    unsafe_allow_html=True,
                )
                st.markdown('<br><br>', unsafe_allow_html=True)

                if stud_percentile > 50:
                    st.write(f"""
                            <h5>You Are in TOP <span style="color: #87CEFA;">{round(100 - stud_percentile, 4)}%</span> Students of University!</h5>
                            """, unsafe_allow_html=True)
                else:
                    st.write(f"""
                            <h5>You Performed better than <span style="color: #87CEFA;">{round(stud_percentile, 4)}%</span> Students of University!</h5>
                            """, unsafe_allow_html=True)

                st.markdown('<br>', unsafe_allow_html=True)

                if stud_brnch_percentile > 50:
                    st.write(f"""
                            <h5>You Are in TOP <span style="color: #87CEFA;">{round(100 - stud_brnch_percentile, 4)}%</span> Students of Your Branch!</h5>
                            """, unsafe_allow_html=True)
                else:
                    st.write(f"""
                            <h5>You Performed better than <span style="color: #87CEFA;">{round(stud_brnch_percentile, 4)}%</span> Students of your Branch</h5>
                            """, unsafe_allow_html=True)


            with r_c:

                st.markdown('<br><br>', unsafe_allow_html=True)

                st_lottie(
                    load_lottieurl(True, "./animation/flying_student.json"),
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="low",  # medium ; high
                    height=None,
                    width=None,
                    key=None,
                )

            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown("---")

            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{stud_branch}'26 </span>and Your CGPA Distribution Stats: </h3>
                        """,
         unsafe_allow_html=True)


            _, left_c, _, right_c, _ = st.columns([1, 3, 1, 3, 1])

            with left_c:

                brnch_cg = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/26_{stud_branch}_ranked_results.csv', index_col=False)

                df = pd.DataFrame({
                    'Branch Stats': ['Highest', 'Average', 'Your', 'Max Appeared'],
                    'CGPA': [max(brnch_cg['Cumulative CGPA'].values), round(statistics.mean(brnch_cg['Cumulative CGPA'].values) ,4),
                             stud_cum_cgpa, round(statistics.mode(brnch_cg['Cumulative CGPA'].values), 4)]})

                df.reset_index(drop=True)
                df.set_index('Branch Stats', inplace=True)

                st.plotly_chart(px.bar(df, title=f"{stud_branch}'26 CGPA Distribution 2026", text_auto='').update_layout({'dragmode':False}), use_container_width=True, config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d', 'zoomOut2d']})

            with right_c:

                uni_cg = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/26_UNI_ranked_results.csv', index_col=False)

                df = pd.DataFrame({
                    'University Stats': ['Highest', 'Average', 'Your', 'Max Appeared'],
                    'CGPA': [max(uni_cg['Cumulative CGPA'].values), round(statistics.mean(uni_cg['Cumulative CGPA'].values) ,4),
                             stud_cum_cgpa, round(statistics.mode(uni_cg['Cumulative CGPA'].values), 4)]})

                df.reset_index(drop=True)
                df.set_index('University Stats', inplace=True)

                st.plotly_chart(px.bar(df, title=f'University CGPA Distribution 2026', text_auto='').update_layout({'dragmode':False}), use_container_width=True,  config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d', 'zoomOut2d', 'hoverClosestCartesian']})

            df1 = pd.DataFrame(
                {
                    'SEMESTER': ['1ST SEM', '2ND SEM', '3RD SEM'],
                    'CGPA': [df_final['SEM1'].values[0], df_final['SEM2'].values[0], df_final['SEM3'].values[0]]
                }
            )

            _, mid , _ =  st.columns([1,2.5,1])
            with mid: st.plotly_chart(px.line(df1, x="SEMESTER", y="CGPA", title='YOUR CGPA CHART: ', range_y=[0,10]).update_layout({'dragmode':False}), use_container_width=True)

            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown("---")


            df = pd.read_csv(
                f'./Extracting_Result_Data/ranked_results_csv/26_{stud_branch}_ranked_results.csv',
                dtype=str,
                index_col=None).fillna("")

            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{stud_branch}'26 </span> Students Rankings: </h3>
                        """,
                     unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            _, mm, _ = st.columns([1, 4, 1])
            dataspace = mm.empty()

            dataspace.dataframe(df, hide_index=True, use_container_width=True, height=450)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")


            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{shortf_branch26[stud_branch]}</span> Placement Stats:</h3>
                        """,
                     unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)


            # data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0] FOR ACCESING VALYE OF PLACEMENT DIRECTLY
            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/average_package21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                'AVERAGE PACKAGE': [
                    data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0],
                    data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0],
                    data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Avg CTC (in LPA)'].values[0]
                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            avg_placement_barc = px.bar(df, title=f"Average Package Trend (IN LPA)", text_auto='').update_layout({'dragmode':False})

            # HIGHEST PLACEMENTS

            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                'HIGHEST PACKAGE': [
                    data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Max CTC (in LPA)'].values[0],
                    data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Max CTC (in LPA)'].values[0],
                    data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Max CTC (in LPA)'].values[0]
                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            max_placement_barc = px.bar(df, title=f"Highest Package Trend (IN LPA)", text_auto='').update_layout({'dragmode':False})

            # PERCENTAGE PLACED PLACEMENT

            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                '% STUDENT PLACED': [
                    float(data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%', '')),
                    float(data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%', '')),
                    float(data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%', ''))
                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            percent_placement_barc = px.bar(df, title=f"Percentage Of Student Placed", range_y=[0,100], text_auto='').update_layout({'dragmode':False})

            bar1, bar2, bar3 = st.columns(3)
            with bar1: st.plotly_chart(avg_placement_barc, use_container_width=True, config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d']})
            with bar2: st.plotly_chart(max_placement_barc, use_container_width=True, config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d']})
            with bar3: st.plotly_chart(percent_placement_barc, use_container_width=True, config={"modeBarButtonsToRemove": [ 'lasso2d', 'autoScale2d', 'select2d']})

            st.markdown("---")

# ELIF CASES FOR CALLING OUT THE OTHER MENU FUNCTIONS!

elif selected=='RANKS':
    ranksNresults_menu()

elif selected=='PLACEMENTS':
    placement_menu()

elif selected=='ABOUT':
    aboutsection_menu()

elif selected=='STUDY':
    studyResources_menu()
