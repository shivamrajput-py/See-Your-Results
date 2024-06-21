import streamlit as st
import json
import pandas as pd
import plotly_express as px
from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
import os
import statistics

import warnings
warnings.filterwarnings('ignore')

shortf_branch26 = {
    'EP': 'Engineering Physics',
    'AE': 'Automotive Engineering',
    'CO': 'Computer Science',
    'IT': 'Information Technology',
    'MC': 'Mathematics and Computing',
    'SE': 'Software Engineering',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electric Engineering',
    'BT': 'Biotech Engineering',
    'EN': 'Envirnomental Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Chemical Engineering',
    'PE': 'Production Engineering',
    'ME': 'Mechanical Engineering'
}
shortf_branch27 = {
    'EP': 'Engineering Physics',
    'AE': 'Automotive Engineering',
    'CS': 'Computer Science',
    'IT': 'Information Technology',
    'MC': 'Mathematics and Computing',
    'SE': 'Software Engineering',
    'EC': 'Electronics and Communication Engineering',
    'EE': 'Electric Engineering',
    'BT': 'Biotech Engineering',
    'EN': 'Envirnomental Engineering',
    'CE': 'Civil Engineering',
    'CH': 'Chemical Engineering',
    'PE': 'Production Engineering',
    'ME': 'Mechanical Engineering'
}

st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='DTU Student Profile', page_icon='🧑‍🎓')

color = '#1F51FF'
other= False

with open('style1.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_lottieurl(isjson: bool, url_or_path: str):
    if isjson:
        with open(url_or_path, 'r') as fl:
            return json.loads(fl.read())
    else:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

lm,mm,_ = st.columns([1,3,1])
with mm:
    selected = option_menu(menu_title=None, options= ['STUDENT PROFILE', 'RESULTS/RANKS', 'ABOUT'],
                           default_index=0,
                           icons=['person-vcard', 'bar-chart-line', 'info-square'],
                           orientation='horizontal'
                           )

with lm:
    st_lottie(
        load_lottieurl(True, "./animation/hat_w_books.json"),
        speed=1,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=80,
        width=80,
        key=None,
    )


#---------------------------MENU: STUDENT PROFILE STARTED-----------------------------------------------------------------------------------------------------------------------

if selected=='STUDENT PROFILE':

    _,srch_middle, _ = st.columns(3)

    title = srch_middle.empty()
    title.write(f"""
    <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2027</h2>
    """,
    unsafe_allow_html=True)

    _, descrip, _ = st.columns([1,3,1])
    descripe = descrip.empty()
    with descripe: st.markdown("""
    <h5 style="text-align: center; align-items: center;">Enter your roll number to access a comprehensive summary of your semester grades and academic performance. A detailed report will be generated upon entry.</h2>
    """, unsafe_allow_html=True)


    _,middle1,middle2, _ = st.columns([2.5,1,1,2.5])
    with middle2:
        st.markdown('<br>', unsafe_allow_html=True)
        result_search_box = st.text_input("Enter Your Roll Number Here", value='', placeholder='__/__/___')
    with middle1:
        st.markdown('<br>', unsafe_allow_html=True)
        year_choosed = st.selectbox("Choose Year", ['2027' ,'2026'], index=0)

    if year_choosed=='2026':
        title.write(f"""
            <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2026</h2>
            """,unsafe_allow_html=True)

    # SPECIAL ADDITION IN THE WEBSITE, KIRTI __________________________________________________________________________________________________________

    if result_search_box and '19012007' == result_search_box:
        descripe.empty()
        other = True
        st.subheader('IS KIRTI :pouting_cat: HERE ? WTF ARE YOU DOING HERE!')
        st.write("I actually don't know whether you are the kri-tikka ik or someone else?")
        st.write('Give me the right answer of the question written below:')
        kiritbox = st.text_input(label='', value='', placeholder='What is that short name that you gave it to yourself, after that i started calling you by that name!')
        if kiritbox:
            if kiritbox == 'kirit' or kiritbox == 'Kirit' or kiritbox == 'KIRIT':
                st.warning("YOU ARE THE KRITIKA :smile_cat: I KNOW, I MEAN KIRIT BKL 🥰")
                kiriti = ['WELCOME TO','MY WEBSITE', 'MISS CERTIFIED', 'BIG W YAPPER', 'KRITIKA SINHA :smirk_cat:']
                for i in range(52):
                    st.markdown("""<br><br>""", unsafe_allow_html=True)
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
                    st.markdown("""<br><br>""", unsafe_allow_html=True)

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
                    st.markdown("""<br><br>""", unsafe_allow_html=True)
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

    # ENDING OF SPECIAL ADDITION IN THE WEBSITE____________________________________________________________________________________________________________

    if year_choosed=='2027' and result_search_box:
        descripe.empty()

        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box= result_search_box.replace('2k', '').replace('2K', '').strip()

        if len(result_search_box)==8:
            result_search_box  = result_search_box[0:6] + '0' + result_search_box[6:]

        jsondf = pd.read_json("./Extracting_Result_Data/extracted_data_json/uniwise_ranked_results.json")
        m1 = jsondf['rolln'].str.contains(result_search_box.upper())
        df_final = jsondf[m1]

        if (len(df_final)>1 or len(df_final)<1) and not other:
            st.markdown('<br><br><br>', unsafe_allow_html=True)
            st.error("No student was found with the provided roll number. Please verify the roll number and try again. If you believe this is a mistake, please contact the Project Maintainer.")
            st.error("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE SHARE (GO TO ABOUT SECTION), I WILL SOLVE IT ASAP!")

        elif len(df_final)==1:

            stud_branch = str(df_final['rolln'].values[0])[3:5]
            stud_sem = 1
            stud_branch_rank = None
            stud_university_rank = None
            with open('./Extracting_Result_Data/extracted_data_json/branchwise_ranked_results.json', 'r') as fl:
                dt = json.loads(fl.read())
                for sd in dt[str(stud_sem)+'_'+str(stud_branch)]:
                    if sd['rolln'] == df_final['rolln'].values[0]:
                        stud_branch_rank = sd['rank']

            with open('./Extracting_Result_Data/extracted_data_json/uniwise_ranked_results.json', 'r') as fl:
                dt = json.loads(fl.read())
                for sd in dt:
                    if sd['rolln'] == df_final['rolln'].values[0]:
                        stud_university_rank = sd['rank']

            stud_percentile = round(float(((2590.0-stud_university_rank)/2589.0)*100), 4)

            l_c ,m_c, r_c = st.columns([1.5,2,1])

            with l_c:

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
                l2.metric(label="Cumulative CGPA" , value=df_final['sgpa'].values[0])

            with m_c:

                st.markdown('<br><br><br>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                | Credits Completed | Cumulative CGPA | University Rank | Branch Rank |
                | :------------ | :--------------- | :---------------| :---------------|
                | {df_final['credits'].values[0]}<br> | {df_final['sgpa'].values[0]}<br> | {stud_university_rank}<br> | {stud_branch_rank}<br> |
                """,
                    unsafe_allow_html=True,
                )
                st.markdown('<br>', unsafe_allow_html=True)

                st.text(f"You performed better than {round(stud_percentile, 6)} Percent Students")

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

            _, left_c, _ , right_c, _ = st.columns([1,3,1,3,1])

            with left_c:

                brnch_cg = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/cg_analysis.csv', index_col=False)

                for brnach_srn, branch_name in enumerate(brnch_cg['BRANCH'].values):
                    if stud_branch in branch_name: i=brnach_srn

                brnch_cg['Your'][i] = df_final['sgpa'].values[0]

                df = pd.DataFrame({
                    'Academic Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [brnch_cg['Highest'].values[i],brnch_cg['Average'].values[i],brnch_cg['Your'].values[i],brnch_cg['Max Appeared'].values[i],brnch_cg['Lowest'].values[i]]})

                df.reset_index(drop=True)
                df.set_index('Academic Stats', inplace=True)

                bar_chrt_l = px.bar(df,title=f'{stud_branch} CGPA Distribution', width=440, height=420)

                st.plotly_chart(bar_chrt_l)


            with right_c:

                uni_cg = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/cg_analysis.csv', index_col=False)
                brnch_cg['Your'][0] = df_final['sgpa'].values[0]

                df = pd.DataFrame({
                    'Academic Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [brnch_cg['Highest'].values[0], brnch_cg['Average'].values[0], brnch_cg['Your'].values[0],brnch_cg['Max Appeared'].values[0], brnch_cg['Lowest'].values[0]]})

                df.reset_index(drop=True)
                df.set_index('Academic Stats', inplace=True)

                bar_chrt_r = px.bar(df, title=f'University CGPA Distribution', width=440, height=420)

                st.plotly_chart(bar_chrt_r)

            #--------------------------------------------------------------------------------------------------------------------------------------------

            st.markdown('<br>', unsafe_allow_html=True)

            df = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_sem}_{stud_branch}_ranked_results.csv', dtype=str,
                             index_col=None).fillna("")

            st.write(f"""
            <h3 style="
            text-align: center;
            align-items: center;
            ">Your Branch <span style="color: {color};">{stud_branch}'{stud_sem+26}</span> Students Rankings: </h3>
            """,
                              unsafe_allow_html=True)

            _,mm,_ = st.columns([1,4,1])
            dataspace = mm.empty()

            dataspace.dataframe(df, hide_index=True, use_container_width=True, height= 450)


    if year_choosed=='2026' and result_search_box:
        descripe.empty()

        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box= result_search_box.replace('2k', '').replace('2K', '').strip()

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

            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/26_{stud_branch}_ranked_results.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper())
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]

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
                l2.metric(label="2ND SEM CG", value=df_final['SEM2'].values[0])
                l3.metric(label="3RD SEM CG", value=df_final['SEM3'].values[0])

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
                st.markdown('<br>', unsafe_allow_html=True)

                st.text(f"You performed better than {round(stud_percentile, 6)} Percent Students")

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

            _, left_c, _, right_c, _ = st.columns([1, 3, 1, 3, 1])

            with left_c:

                brnch_cg = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/26_{stud_branch}_ranked_results.csv', index_col=False)

                df = pd.DataFrame({
                    'Academic Stats': ['Highest', 'Average', 'Your', 'Max Appeared'],
                    'CGPA': [max(brnch_cg['Cumulative CGPA'].values), round(statistics.mean(brnch_cg['Cumulative CGPA'].values) ,4),
                             stud_cum_cgpa, round(statistics.mode(brnch_cg['Cumulative CGPA'].values), 4)]})

                df.reset_index(drop=True)
                df.set_index('Academic Stats', inplace=True)

                bar_chrt_l = px.bar(df, title=f'{stud_branch} CGPA Distribution 2026', width=440, height=420)

                st.plotly_chart(bar_chrt_l)

            with right_c:

                uni_cg = pd.read_csv('./Extracting_Result_Data/ranked_results_csv/26_UNI_ranked_results.csv', index_col=False)

                df = pd.DataFrame({
                    'Academic Stats': ['Highest', 'Average', 'Your', 'Max Appeared'],
                    'CGPA': [max(uni_cg['Cumulative CGPA'].values), round(statistics.mean(uni_cg['Cumulative CGPA'].values) ,4),
                             stud_cum_cgpa, round(statistics.mode(uni_cg['Cumulative CGPA'].values), 4)]})

                df.reset_index(drop=True)
                df.set_index('Academic Stats', inplace=True)

                bar_chrt_r = px.bar(df, title=f'University CGPA Distribution 2026', width=440, height=420)

                st.plotly_chart(bar_chrt_r)

            st.markdown('<br>', unsafe_allow_html=True)

            df = pd.read_csv(
                f'./Extracting_Result_Data/ranked_results_csv/26_{stud_branch}_ranked_results.csv',
                dtype=str,
                index_col=None).fillna("")


            st.markdown('<br>', unsafe_allow_html=True)

            df1 = pd.DataFrame(
                {
                    'SEMESTER': ['1ST SEM', '2ND SEM', '3RD SEM'],
                    'CGPA': [df_final['SEM1'].values[0], df_final['SEM2'].values[0], df_final['SEM3'].values[0]]
                }
            )
            # df1.reset_index(drop=True)
            # df1.set_index('SEMESTER', inplace=True)

            cg_line_chart = px.line(df1, x="SEMESTER", y="CGPA", title='YOUR CGPA CHART: ', range_y=[0,10])

            _, mid , _ =  st.columns([1,2.5,1])
            with mid: st.plotly_chart(cg_line_chart, use_container_width=True)


            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{stud_branch}'26 </span> Students Rankings: </h3>
                        """,
                     unsafe_allow_html=True)

            _, mm, _ = st.columns([1, 4, 1])
            dataspace = mm.empty()

            dataspace.dataframe(df, hide_index=True, use_container_width=True, height=400)


#------------------------------MENU: UNIVERSITY RANK STARTED--------------------------------------------------------------------------------------------------------------


elif selected=='RESULTS/RANKS':

    lf, rt = st.columns([0.5, 3])

    with lf:
        st.markdown('<br><br><br>', unsafe_allow_html=True)

        year_choosed = st.selectbox('Choose Year', ['2027', '2026'] ,index=0)
        if year_choosed=='2026': shortf_branch = shortf_branch26
        elif year_choosed=='2027': shortf_branch = shortf_branch27

        brnch_choosed = st.selectbox('Choose Branch', ['Cumulative'] + list(shortf_branch.values()),
                                     index=0)

        text_search = st.text_input(label="Enter Roll Number Or Name To Search Students", value="")

    if brnch_choosed:
        if brnch_choosed == 'Cumulative':
            if year_choosed=='2026':
                flname, title_help = f'26_UNI_ranked_results.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking 2026'
            elif year_choosed=='2027':
                flname, title_help = f'1_UNI_ranked_results.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking 2027'
        else:
            for key in shortf_branch.keys():
                if shortf_branch[key] == brnch_choosed:
                    if year_choosed=='2027':
                        flname = f'1_{key}_ranked_results.csv'
                        title_help = f'<span style="color: {color};">{shortf_branch[key]}</span> Students CGPA Ranking 2027'
                    elif year_choosed=='2026':
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
    dataspace.dataframe(df, hide_index=True, height=525, use_container_width=True)

    # Filter the dataframe using masks !!!!!!!!! GOTT THIS FROM INTERNET! PLEASE LEARN PANDAS TO UNDERSTAND THIS
    m1 = df["NAME"].str.contains(text_search.upper())
    m2 = df["ROLL NO."].str.contains(text_search.upper())
    df_search = df[m1 | m2]

    # Show the results, if you have a text_search
    if text_search:
        dataspace.dataframe(df_search, hide_index=True, height=525, use_container_width=True)

#--------------------------------MENU: ABOUT STARTED------------------------------------------------------------------------------------------------------------------


elif selected=='ABOUT':
    lc, rc  = st.columns([1.3,1])

    with rc:
        st_lottie(
            load_lottieurl(True,"./animation/boyy_with_laptop.json"),
            speed=1,
            reverse=False,
            loop=True,
            quality="low",  # medium ; high
            height=None,
            width=None,
            key=None,
        )

        st.write('<h5>This Website is Developed and Maintained By ME.</h5>', unsafe_allow_html=True)
        l_, m_, r_ = st.columns([6, 2.5, 2.5])

        with l_:
            st.write(f"""
                            <h4>Hey, SHIVAM Here<br>Engineering Physics 2027</h4>
                            """,
                     unsafe_allow_html=True)

        with m_:
            st.markdown('######')
            st.markdown(
                '''<a id="social1" href="https://www.instagram.com/shivammm20_/"><button class="button-62" type="button">INSTAGRAM</button>''',
                unsafe_allow_html=True)

        with r_:
            st.markdown('######')
            st.markdown(
                '''<a id="social2" href="https://www.linkedin.com/in/shivam-rajput-3928a328a/"><button class="button-18" type="button">  LINKDIN  </button>''',
                unsafe_allow_html=True)

    with lc:

        st.write(f"""
        <h1 class="nametit">Your Education<br>Dashboard<br>DTU RESULTS</h1>
                <br>""", unsafe_allow_html=True)


        st.markdown('<br>', unsafe_allow_html=True)

        st.write(f"""
            <h3 class="about">MORE <span style="color: yellow;">FEATURES</span> TO COME, IN FURTHER UPDATES</h3>
            <h6 class="about">- 2nd Sem results ? YES I WILL UPDATE, After Results, ASAP!</h6>
            <h6 class="about">- What about 2025 Results etc? YES I am going to add them too, it will take time. </h6>
            <h6 class="about">- Placement Stats, of all the past years and current year, of all the branch.</h6>
            <h6 class="about">- Study Material and Resources that will help during exams</h6>
            <h6 class="about">- Other than this, Suggest me what more should i add ?</h6>
            """,
         unsafe_allow_html=True)

        st.markdown('<br><br><br>', unsafe_allow_html=True)

        st.warning("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF'S, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR YOU FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE SHARE (GO TO ABOUT SECTION), I WILL SOLVE IT ASAP!")

#---------------------------------------------------END-----------------------------------------------------------------------------------------------