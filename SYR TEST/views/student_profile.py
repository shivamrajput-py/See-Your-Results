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
# warnings.filterwarnings('ignore')
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
    result_search_box = st.text_input("Enter Your Roll Number Here", value='', placeholder='__/__/___')

if year_choosed=='2026':
    Mtitle.write(f"""
        <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2026</h2>
        """,unsafe_allow_html=True)


#-----------------------------SPECIAL ADDITION IN THE WEBSITE, KIRTI--------------------------------------------------------------------------------------------------------

if result_search_box:

    # VIEW COUNTING
    if countedview == 0 and WEBONSERVER:
        countedview += 1
        with open('user_webViewsData.txt', 'a') as fl:
            fl.write(f"""USER AT {datetime.datetime.now()} SEARCHED "{result_search_box}"\n""")
            fl.flush()
    elif countedview==1:
        with open('user_webViewsData.txt', 'a') as fl:
            fl.write(f"""SAME USER SEARCHED "{result_search_box}"\n""")
            fl.flush()


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

        # st.markdown('<br>', unsafe_allow_html=True)
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

    data26std = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/26Batch_allStudent.csv')
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

            uni_cg = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/26Batch_allStudent.csv', index_col=False)

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