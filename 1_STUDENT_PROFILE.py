import streamlit as st
import json
import pandas as pd
import plotly_express as px
from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
import os

shortf_branch = {
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

color = '#1F51FF'
st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='DTU Student Profile', page_icon='🧑‍🎓')

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

other= False

#---------------------------MENU: STUDENT PROFILE STARTED-----------------------------------------------------------------------------------------------------------------------

if selected=='STUDENT PROFILE':

    _,srch_middle, _ = st.columns(3)

    srch_middle.write(f"""
    <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2027</h2>
    """,
    unsafe_allow_html=True)

    _, descrip, _ = st.columns([1,3,1])
    descripe = descrip.empty()
    with descripe: st.markdown("""
    <h5 style="text-align: center; align-items: center;">Enter your roll number to access a comprehensive summary of your semester grades and academic performance. A detailed report will be generated upon entry.</h2>
    """, unsafe_allow_html=True)

    _,middle, _ = st.columns([2,1,2])
    with middle:
        st.markdown('<br>', unsafe_allow_html=True)
        result_search_box = st.text_input("Enter Your Roll Number Here", value='', placeholder='23/__/___')

    if result_search_box:
        descripe.empty()

        # FUN --------------------- ADDITION IN THE WEBAPP __________________________________________________
        if '19012007' == result_search_box:
            other= True
            st.subheader('IG KIRTI IS HERE ? 😠')
            st.text('I actually do not know you are real kirti or not?')
            st.text('Give me the right answer of the question down below:')
            kiritbox = st.text_input('What is that short name that you gave it to yourself, after that i started calling you by that name!')
            if kiritbox:
                if kiritbox=='kirit' or kiritbox=='Kirit' or kiritbox=='KIRIT':
                    st.warning("YOU AREEEE ACTUALLY KIRTI, I MEAN KIRIT BKL 🥰")
                else:
                    st.warning("EITHER YOU ARE NOT KIRTI OR YOU ARE, BUT YOU DON'T KNOW THE ANSWER ! L KIRTI L KIRTI ")
        # FUN --------------------- ADDITION IN THE WEBAPP __________________________________________________


        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box= result_search_box.replace('2k', '').replace('2K', '').strip()


        jsondf = pd.read_json("./Extracting_Result_Data/extracted_data_json/uniwise_ranked_results.json")
        m1 = jsondf['rolln'].str.contains(result_search_box.upper())
        df_final = jsondf[m1]

        if (len(df_final)>1 or len(df_final)<1) and not other:
            st.markdown('<br><br><br>', unsafe_allow_html=True)
            st.error("No student was found with the provided roll number. Please verify the roll number and try again. If you believe this is a mistake, please contact the Project Maintainer.")
            st.error("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE SHARE (GO TO ABOUT SECTION), I WILL SOLVE IT ASAP!")

        elif len(df_final)==1:

            stud_branch = str(df_final['rolln'].values[0])[3:5]
            stud_sem = int(str(df_final['rolln'].values[0])[:2]) - 22
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
                <h2 class="nametit">HELLO, {df_final['name'].values[0]}</h2>
                <h5>{stud_branch}, {shortf_branch[stud_branch]}, B. TECH</h5>
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

            dataspace.dataframe(df, hide_index=True, use_container_width=True, height= 400)


#------------------------------MENU: UNIVERSITY RANK STARTED--------------------------------------------------------------------------------------------------------------


elif selected=='RESULT/RANKS':

    lf, rt = st.columns([1, 3])

    with lf:
        st.markdown('<br><br><br>', unsafe_allow_html=True)

        year_choosed = st.selectbox('Choose Year', ['2027'], index=0)
        brnch_choosed = st.selectbox('Choose Branch', ['Cumulative'] + list(shortf_branch.values()),
                                     index=0)

        text_search = st.text_input(label="Enter Roll Number/Name to Find a specific student", value="",
                                placeholder="23/__/___")


    if brnch_choosed:
        if brnch_choosed == 'Cumulative':
            flname, title_help = f'uniwise_ranked_results.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking'
        else:
            for key in shortf_branch.keys():
                if shortf_branch[key] == brnch_choosed:
                    flname = f'1_{key}_ranked_results.csv'
                    title_help = f'<span style="color: {color};">{shortf_branch[key]}</span> Students CGPA Ranking'

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
    lc, rc  = st.columns([1.5,1])

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


    with lc:

        st.write(f"""
            <h2 class="nametit">HEY, SHIVAM Here</h2>
            <h5>Engineering Physics 2027</h5>
            <h5>I hope you liked my project, I would love to hear your feedback and suggestion on this one</h5>
            
            """,
            unsafe_allow_html=True)

        st.markdown("<h5>Contact Me Here:</h5>", unsafe_allow_html=True)

        M1,M2,_ = st.columns([3,3,14])

        with M1:
            st.markdown('''<a id="social1" href="https://www.instagram.com/shivammm20_/"><button class="button-62" type="button">INSTAGRAM</button>''', unsafe_allow_html=True)

        with M2:
            st.markdown('''<a id="social2" href="https://www.linkedin.com/in/shivam-rajput-3928a328a/"><button class="button-18" type="button">  LINKDIN  </button>''', unsafe_allow_html=True)



        st.markdown('<br><br><br>', unsafe_allow_html=True)

        st.write(f"""
            <h3 class="about">MORE <span style="color: yellow;">FEATURES</span> TO COME, IN FURTHER UPDATES</h3>
            <h6>- 2nd Sem results ? YES I WILL UPDATE, After Results, ASAP!</h6>
            <h6>- What about 2026,2025 Results etc? YES I am going to add them too, it will take time. </h6>
            <h6>- Placement Stats, of all the past years and current year, of all the branch.</h6>
            <h6>- Study Material and Resources that will help during exams</h6>
            <h6>- Other than this, Suggest me what more should i add ?</h6>
            """,
         unsafe_allow_html=True)

        st.markdown('<br><br><br>', unsafe_allow_html=True)

        st.warning("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF'S, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR YOU FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE SHARE (GO TO ABOUT SECTION), I WILL SOLVE IT ASAP!")

#---------------------------------------------------END-----------------------------------------------------------------------------------------------