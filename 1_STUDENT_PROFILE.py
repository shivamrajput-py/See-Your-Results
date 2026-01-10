import csv
import random
import time
import streamlit as st
import json
import pandas as pd
import plotly_express as px
from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
from MainConstant import *
import os
from datetime import datetime
import statistics
import warnings
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import base64

warnings.filterwarnings('ignore')

st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='DTURESULTS ANALYSIS', page_icon='🎓')

color = '#1F51FF'  # USE FOR HIGHLIGHTING A SPECIFIC WORD
BAR_COLOR = '#1E90FF'
other = False
st.session_state.yeartitle = '2028'

with open('style.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------------------

# FOR LOADING THE ANIMATION !!!!
@st.fragment
def load_lottieurl(isjson: bool, url_or_path: str):
    if isjson:
        with open(url_or_path, 'r') as fl:
            return json.loads(fl.read())
    else:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


@st.fragment
def find(SUBC: str, TYPE: str, sendsorted=True) -> dict:
    SUBJECT_GROUP_STR = [" CO101 | CO102 | CO116 | CO105 ", ]

    for sub_grp in SUBJECT_GROUP_STR:
        if SUBC in sub_grp:
            SUBC = sub_grp

    with open(r'./Extracting_Result_Data/StudyMaterialData/DATA_MAIN2.json', 'r') as fl:
        doc = json.load(fl)

    if SUBC in doc[0][TYPE].keys():
        req_dic = {}
        if sendsorted:
            for key in doc[0][TYPE][SUBC].keys():
                if doc[0][TYPE][SUBC][key] != "":
                    req_dic[key] = doc[0][TYPE][SUBC][key]

            return req_dic
        else:
            return doc[0][TYPE][SUBC]
    else:
        return False

# -----------------------------------------------------------------------------------------------------------------------

# SGPA CALCULATOR FUNCTION WITH A DIALOG
@st.dialog("GAINERS LIST", width="large")
def gainerList(stud_branch: str):
    df = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_gainersR27.csv', dtype=str).fillna("")
    df = df[['RANK', 'NAME', 'ROLL NO.', 'SEM3', 'SEM4', 'IMPROVEMENT']]
    df.columns = ['RANK', 'NAME', 'ROLL NO.', 'SEM 3', 'SEM 4', 'CGPA IMPROVEMENT']

    st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        "><span style="color: {color};">{stud_branch}'27</span> Top Gainers: </h3>
                        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    ranklist = st.empty()
    ranklist.dataframe(df, hide_index=True, use_container_width=True, height=460)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('---')

# ----------------------------------------------------------------------------------------------------------------------
# PDF PART !!
# ----------------------------------------------------------------------------------------------------------------------
# PDF PART !!

# Function to create PDF report card
def create_report_card_pdf(student_data):
    """
    Creates a PDF report card for the student
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )

    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    # Title
    title = Paragraph("DELHI TECHNOLOGICAL UNIVERSITY", title_style)
    subtitle = Paragraph("ACADEMIC REPORT CARD", header_style)
    elements.append(title)
    elements.append(subtitle)
    elements.append(Spacer(1, 20))

    # Student Information
    student_info = [
        ['Student Name:', student_data['name']],
        ['Roll Number:', student_data['roll_no']],
        ['Branch:', f"{student_data['branch']} - {student_data['branch_full']}"],
        ['Academic Year:', student_data['year']],
        # ['Report Generated:', datetime.now().strftime("%d-%m-%Y %H:%M")]
    ]

    info_table = Table(student_info, colWidths=[2 * inch, 3 * inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Academic Performance Summary
    elements.append(Paragraph("ACADEMIC PERFORMANCE SUMMARY", header_style))
    elements.append(Spacer(1, 10))

    performance_data = [
        ['Metric', 'Value'],
        ['Cumulative CGPA', str(student_data['cumulative_cgpa'])],
        ['Total Credits Completed', str(student_data['total_credits'])],
        ['University Rank', str(student_data['university_rank'])],
        ['Department Rank', str(student_data['department_rank'])],
        ['University Percentile', f"{student_data['university_percentile']}%"],
        ['Department Percentile', f"{student_data['department_percentile']}%"]
    ]

    performance_table = Table(performance_data, colWidths=[2.5 * inch, 2.5 * inch])
    performance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(performance_table)
    elements.append(Spacer(1, 20))

    # Semester-wise Results
    elements.append(Paragraph("SEMESTER-WISE ACADEMIC RECORD", header_style))
    elements.append(Spacer(1, 10))

    semester_data = [
        ['Semester', 'SGPA', 'Credits', 'Status']
    ]

    for i, sem_data in enumerate(student_data['semesters'], 1):
        semester_data.append([
            f'Semester {i}',
            str(sem_data['sgpa']),
            str(sem_data['credits']),
            'Completed'
        ])

    semester_table = Table(semester_data, colWidths=[1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch])
    semester_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(semester_table)
    elements.append(Spacer(1, 30))

    # Footer
    footer_text = """
    This is a computer-generated report card based on the available data. 
    For any queries, please contact through the about section.
    """
    footer = Paragraph(footer_text, normal_style)
    elements.append(footer)

    elements.append(Spacer(1, 10))

    footer_date_gen = Paragraph(f'Report Generated: {datetime.now().strftime("%d-%m-%Y %H:%M")}', normal_style)
    elements.append(footer_date_gen)
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


# Function to display report card dialog
def show_report_card_dialog(student_data):
    """
    Shows a modal dialog with report card information
    """
    with st.expander("📄 STUDENT REPORT CARD", expanded=True):

        # Header Section
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #1e3c72, #2a5298); border-radius: 10px; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">DELHI TECHNOLOGICAL UNIVERSITY</h2>
            <h4 style="color: #e8f4fd; margin: 5px 0;">ACADEMIC REPORT CARD</h4>
        </div>
        """, unsafe_allow_html=True)

        # Student Information
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📋 STUDENT INFORMATION**")
            st.write(f"**Name:** {student_data['name']}")
            st.write(f"**Roll Number:** {student_data['roll_no']}")
            st.write(f"**Branch:** {student_data['branch']} - {student_data['branch_full']}")

        with col2:
            st.markdown("**📊 ACADEMIC SUMMARY**")
            st.write(f"**CGPA:** {student_data['cumulative_cgpa']}")
            st.write(f"**Credits:** {student_data['total_credits']}")
            st.write(f"**University Rank:** {student_data['university_rank']}")

        st.markdown("---")

        # Performance Metrics
        st.markdown("**🎯 PERFORMANCE METRICS**")

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.metric("Department Rank", student_data['department_rank'])
        with metric_col2:
            st.metric("University Percentile", f"{student_data['university_percentile']}%")
        with metric_col3:
            st.metric("Department Percentile", f"{student_data['department_percentile']}%")
        with metric_col4:
            st.metric("Total Credits", student_data['total_credits'])

        st.markdown("---")

        # Semester Performance
        st.markdown("**📚 SEMESTER-WISE PERFORMANCE**")

        semester_df = pd.DataFrame({
            'Semester': [f'SEM {i + 1}' for i in range(len(student_data['semesters']))],
            'SGPA': [sem['sgpa'] for sem in student_data['semesters']],
            'Credits': [sem['credits'] for sem in student_data['semesters']],
            'Status': ['Completed'] * len(student_data['semesters'])
        })

        st.dataframe(semester_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Download Section
        st.markdown("**📥 DOWNLOAD REPORT CARD**")

        # Generate PDF and provide download button AND GG
        try:

            pdf_buffer = create_report_card_pdf(student_data)

            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_buffer.getvalue(),
                    file_name=f"Report_Card_{student_data['roll_no']}.pdf",
                    mime="application/pdf",
                    type="primary"
                )

            with col3:
                st.markdown(f"""
                <small style="color: #666;">
                Report generated on: {datetime.now().strftime("%d-%m-%Y at %H:%M")}
                </small>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            st.info("Please try again or contact support if the issue persists.")


# Alternative approach using session state for better UX jjj IJBFSFJSBS
def add_report_card_button(df_final, stud_branch, shortf_branch27, stud_university_rank,
                           stud_branch_rank, stud_percentile, stud_brnch_percentile,
                           stud_total_credits):
    """
    Add report card button to your existing results display
    """

    # Initialize session state
    if 'show_report_card' not in st.session_state:
        st.session_state.show_report_card = False

    # Add this after your existing student info display
    st.markdown("---")

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("📄 GENERATE REPORT CARD", type="primary", use_container_width=True):
            st.session_state.show_report_card = True

    # Show report card if button was clicked
    if st.session_state.show_report_card:
        # Prepare student data
        student_data = {
            'name': df_final['NAME'].values[0],
            'roll_no': df_final['ROLL NO.'].values[0],
            'branch': stud_branch,
            'branch_full': shortf_branch27[stud_branch],
            'year': '2027',  # or get from year_choosed
            'cumulative_cgpa': df_final['CUMULATIVE CGPA'].values[0],
            'total_credits': stud_total_credits,
            'university_rank': stud_university_rank,
            'department_rank': stud_branch_rank,
            'university_percentile': stud_percentile,
            'department_percentile': stud_brnch_percentile,
            'semesters': [
                {'sgpa': df_final['SGPA1'].values[0], 'credits': df_final['CREDITS1'].values[0]},
                {'sgpa': df_final['SGPA2'].values[0], 'credits': df_final['CREDITS2'].values[0]},
                {'sgpa': df_final['SGPA3'].values[0], 'credits': df_final['CREDITS3'].values[0]},
                {'sgpa': df_final['SGPA4'].values[0], 'credits': df_final['CREDITS4'].values[0]}
            ]
        }

        # Show report card dialog
        show_report_card_dialog(student_data)


# Simpler direct download approach (alternative)
def add_direct_download_button(df_final, stud_branch, shortf_branch27, stud_university_rank,
                               stud_branch_rank, stud_percentile, stud_brnch_percentile,
                               stud_total_credits):
    """
    Direct download approach - generates PDF immediately when clicked
    """
    st.markdown("---")

    # Prepare student data
    student_data = {
        'name': df_final['NAME'].values[0],
        'roll_no': df_final['ROLL NO.'].values[0],
        'branch': stud_branch,
        'branch_full': shortf_branch27[stud_branch],
        'year': '2027',
        'cumulative_cgpa': df_final['CUMULATIVE CGPA'].values[0],
        'total_credits': stud_total_credits,
        'university_rank': stud_university_rank,
        'department_rank': stud_branch_rank,
        'university_percentile': stud_percentile,
        'department_percentile': stud_brnch_percentile,
        'semesters': [
            {'sgpa': df_final['SGPA1'].values[0], 'credits': df_final['CREDITS1'].values[0]},
            {'sgpa': df_final['SGPA2'].values[0], 'credits': df_final['CREDITS2'].values[0]},
            {'sgpa': df_final['SGPA3'].values[0], 'credits': df_final['CREDITS3'].values[0]},
            {'sgpa': df_final['SGPA4'].values[0], 'credits': df_final['CREDITS4'].values[0]}
        ]
    }

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            pdf_buffer = create_report_card_pdf(student_data)
            st.download_button(
                label="📄 Download Report Card (PDF)",
                data=pdf_buffer.getvalue(),
                file_name=f"Report_Card_{student_data['roll_no']}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            st.info("Please try refreshing the page if the issue persists.")

# SGPA CALCULATOR FUNCTION WITH A EXPERIMENTAL DIALOG
@st.dialog("SGPA CALCULATOR", width="small")
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

    if nofs:
        st.session_state.crList = []
        st.session_state.grdList = []

        num = ([4] * (int(nofs) - 1)) + [2, 2]

        for i in range(int(nofs) + 1):
            sec1, sec2 = st.columns([1, 1])

            with sec1:
                if i == 0:
                    pass
                else:
                    crd = st.number_input(f"Subject {i} Credits:", placeholder='Credits:', min_value=0, step=1,value=num[i])
                    st.session_state.crList.append(crd)

            with sec2:
                if i == 0:
                    pass
                else:
                    grd = st.selectbox(f'Subject {i} Grade:', ['O', 'A+', 'A', 'B+', 'B', 'C', 'P', 'F'], index=0)
                    st.session_state.grdList.append(grd)

            st.markdown("---")

# -----------------------------------------------------------------------------------------------------------------------
@st.fragment
def ranksNresults_menu():
    lf, rt = st.columns([0.5, 3])

    with lf:
        st.markdown('<br>', unsafe_allow_html=True)

        year_choosed = st.selectbox('Choose Year', ['2028', '2027', '2026'], index=0)
        if year_choosed == '2026':
            shortf_branch = shortf_branch26
        elif year_choosed == '2027':
            shortf_branch = shortf_branch27
        elif year_choosed == '2028':
            shortf_branch = shortf_branch28

        brnch_choosed = st.selectbox('Choose Branch', ['Cumulative'] + list(shortf_branch.values()), index=0)

        text_search = st.text_input(label="Enter Roll Number Or Name To Search Students", value="")

    if brnch_choosed:
        if brnch_choosed == 'Cumulative':
            if year_choosed == '2026':
                flname, title_help = f'UNI_rankedR26.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking 2026'
            elif year_choosed == '2027':
                flname, title_help = f'UNI_rankedR27.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking 2027'
            elif year_choosed == '2028':
                flname, title_help = f'UNI_rankedR28.csv', f'<span style="color: {color};">UNIVERSITY WISE</span> Students CGPA Ranking 2028'
        else:
            for key in shortf_branch.keys():
                if shortf_branch[key] == brnch_choosed:
                    if year_choosed == '2027':
                        flname = f'{key}_rankedR27.csv'
                        title_help = f'<span style="color: {color};">{shortf_branch[key]}</span> Students CGPA Ranking 2027'
                    elif year_choosed == '2026':
                        flname = f'{key}_rankedR26.csv'
                        title_help = f'<span style="color: {color};">{shortf_branch[key]}</span> Students CGPA Ranking 2026'
                    elif year_choosed == '2028':
                        flname = f'{key}_rankedR28.csv'
                        title_help = f'<span style="color: {color};">{shortf_branch[key]}</span> Students CGPA Ranking 2028'

    rt.write(f"""<h3 style="text-align: center; align-items: center;">{title_help}</h3>""", unsafe_allow_html=True)

    df = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{flname}', dtype=str, index_col=None).fillna("")

    if year_choosed == '2027':
        df = df[['RANK', 'NAME', 'ROLL NO.', 'SGPA1', 'SGPA2', 'SGPA3', 'SGPA4', 'CUMULATIVE CGPA']]
        df.columns = ['RANK', 'NAME', 'ROLL NO.', '1ST SEM', '2ND SEM', '3RD SEM', '4TH SEM', 'CUMULATIVE CGPA']
    elif year_choosed == '2026':
        df = df[['RANK', 'NAME', 'ROLL NO.', 'SGPA1', 'SGPA2', 'SGPA3', 'SGPA4', 'CUMULATIVE CGPA']]
        df.columns = ['RANK', 'NAME', 'ROLL NO.', 'SEM 1', 'SEM 2', 'SEM 3', 'SEM 4', 'CUMULATIVE CGPA']
    elif year_choosed == '2028':
        df = df[['RANK', 'NAME', 'ROLL NO. OG', 'SGPA1', 'SGPA1']]
        df.columns = ['RANK', 'NAME', 'ROLL NO.', '1ST SEM', 'CUMULATIVE CGPA']

    dataspace = rt.empty()
    dataspace.dataframe(df, hide_index=True, height=900, use_container_width=True)

    # Show the results, if you have a text_search
    if text_search:

        # IF USER HAS PUTTEN 2K/2k IN THE ROLL NUMBER, REMOVING THAT CAUSE, OUR DATA DOES NOT CONTAIN THAT
        if '2k' in text_search or '2K' in text_search:
            text_search = text_search.replace('2k', '').replace('2K', '').strip()

        # DEALING WITH USER PUTTEN ROLL NO. 23/EP/12 AND 23/EP/01 for 2026/2027, 24/B12/4 AND 24/B12/04 for 2028
        if year_choosed in ['2026', '2027'] and len(text_search) == 8:
            text_search = text_search[0:6] + '0' + text_search[6:]
        elif year_choosed == '2028' and len(text_search) == 9:
            text_search = text_search[0:7] + '0' + text_search[7:]

        # Filter the dataframe using masks
        m1 = df["NAME"].str.contains(text_search.upper())
        if year_choosed == '2028':
            m2 = df["ROLL NO."].str.contains(text_search.upper())
            df_search = df[m1 | m2]
            dataspace.dataframe(df_search, hide_index=True, height=525, use_container_width=True)
        else:
            m2 = df["ROLL NO."].str.contains(text_search.upper())
            df_search = df[m1 | m2]
            dataspace.dataframe(df_search, hide_index=True, height=525, use_container_width=True)

# -----------------------------------------------------------------------------------------------------------------------

# PLACEMENT STATS MENU
@st.fragment
def placement_menu():
    # ----------------------------- 2023 PALCEMENTS ----------------------------------------------

    st.write(f"""
                <h6 style="
                text-align: center;
                align-items: center;
                font-size: 13px;
                ">Be on Desktop mode to see the graphs properly! (2024 STATS SOON!)</h6>
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
        st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2023', text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
            {'dragmode': False}), use_container_width=True, config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']})

    data23 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package23.csv').dropna()

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Max CTC (in LPA)': data23['Max CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with l:
        st.plotly_chart(px.bar(df, title='Highest Package from Every Branch in 2023', text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
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
                               range_y=[0, 100], color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}), use_container_width=True,
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
        st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2022', text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
            {'dragmode': False}), use_container_width=True, config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']})

    data22 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package22.csv').dropna()

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Max CTC (in LPA)': data22['Max CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with l1:
        st.plotly_chart(px.bar(df, title='Highest Package from Every Branch in 2022', text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
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
                               text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),
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
        st.plotly_chart(px.bar(df, title='Average Package of Every Branch in 2021', text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
            {'dragmode': False}), config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}, use_container_width=True)

    data21 = pd.read_csv('./Extracting_Result_Data/placement_data/highest_package21.csv').dropna()

    df = pd.DataFrame({
        'Branch': ['BT', 'CE', 'CS', 'EE', 'ECE', 'EP', 'ENE', 'IT', 'MAC', 'ME', 'AE', 'CH', 'PIE', 'SE'],
        'Max CTC (in LPA)': data21['Max CTC (in LPA)'].values
    })

    df.reset_index(drop=True)
    df.set_index('Branch', inplace=True)

    with l2:
        st.plotly_chart(px.bar(df, title='Highest Package from Every Branch in 2021', text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
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
                               text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),
                        config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}, use_container_width=True)

    st.markdown("""<br>""", unsafe_allow_html=True)
    st.markdown("---")

# -----------------------------------------------------------------------------------------------------------------------

# STUDY RESORUCES MATERIALS MENU FUNCTION

@st.fragment
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
                    ">WE ARE WORKING ON ADDING BEST RESOURCES. IT IS TAKING TIME, I HOPE YOU GUYS UNDERSTAND!</h6>
                    """,
             unsafe_allow_html=True)

    st.markdown("---")

    s1, s2, s3, s4 = st.columns(4)
    st.markdown("---")

    with open("./Extracting_Result_Data/StudyMaterialData/DATA_MAIN1.json", 'r') as fl:
        DATA = json.load(fl)

    with s1:
        RESOURCE_BRNCH = st.selectbox("CHOOSE BRANCH: ", shortf_branch27.values(), placeholder='BRANCH')

    if RESOURCE_BRNCH:
        RESOURCE_BRNCH = shortf_branch27REV[RESOURCE_BRNCH]
        RESOURCE_SEM = "2"
        with study_mtitle:
            st.write(f"""
                        <h2 style="text-align: center; align-items: center; padding-top: 5px; padding-botton: 5px
                        "><span style="color: {color};"></span>[ {RESOURCE_BRNCH} | SEM{RESOURCE_SEM} ] STUDY MATERIALS</h2>
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
                                "><span style="color: {color};">[ {RESOURCE_BRNCH} | SEM{RESOURCE_SEM} ] </span>STUDY MATERIAL</h2>
                                """, unsafe_allow_html=True)

                if RESOURCE_SUBJECT:
                    with s4:
                        RESOURCE_TYPE = st.selectbox("CHOOSE TYPE: ",
                                                     ['PYQ', 'NOTES', 'PLAYLISTS', 'ASSIGNMENTS', 'BOOKS'], index=0,
                                                     placeholder='TYPE')

                    RESOURCE_SUBCODE = DATA[0][RESOURCE_BRNCH][RESOURCE_SEM][RESOURCE_SUBJECT]

                    if RESOURCE_SUBCODE != "NONE":

                        with open('./Extracting_Result_Data/StudyMaterialData/DATA_MAIN2.json', 'r') as fl2:
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

# -----------------------------------------------------------------------------------------------------------------------

# ABOUT SECTIOO OF MAIN MENU FUNCTION STARTS

def aboutsection_menu():
    lc, rc = st.columns([1.3, 1])

    with rc:
        st.write('<h6>This Website is Developed and Maintained By Shivam Rajput.</h6>', unsafe_allow_html=True)
        l_, m_, r_ = st.columns([5, 2.5, 2.5])

        st_lottie(
            load_lottieurl(True, "./animation/boy_workingBack.json"),
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=None,
            width=530, )

        with l_:
            st.write(f"""
                    <h4>Hey, Shivam Here<br>Engineering Physics 2027</h4>
                    """,
                     unsafe_allow_html=True)

        with m_:
            st.markdown('######')
            st.markdown(
                '''<a class="social1_" href="https://www.instagram.com/shvmm203/"><button class="button-62" type="button">INSTA</button>''',
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

        st.write(f"""
                <h3 class="about">MORE <span style="color: #1F51FF;">FEATURES</span> TO COME IN FUTURE UPDATES</h3>
                <h6 class="about">- 2026 & 2028 Batch Results? These will be updated soon!</h6>
                <h6 class="about">- Report Card Feature? This feature has been added!</h6>
                <h6 class="about">- Other than this, Suggest me what more should i add ?</h6>
                """,
                 unsafe_allow_html=True)

        st.markdown('<br><br><br>', unsafe_allow_html=True)

    # st.warning("I HAVE EXTRACTED RESULT DATA FROM RESULT PDF'S, SO IF YOU ARE UNABLE TO FIND YOUR RESULT OR YOU FIND ANY ERROR RELATED TO YOUR RESULT, PLEASE CONTACT ME, I WILL SOLVE IT ASAP!")

# -----------------------------------------------------------------------------------------------------------------------

# MAIN EXECUTION CODE STARTS FROM HER

# MAIN MENU COLUMNS FOR LOGO ANIMATION AND REAL MAIN MENU
mainmenu_left, mainmenu_middle, _ = st.columns(spec=[0.8, 3, 0.8])

with mainmenu_left:
    pass
    # st.image("") CAN PUT YOUR LOGO HERE !!!

    st_lottie(
        load_lottieurl(True, "./animation/hat_w_books.json"),
        speed=0.8,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=80,
        width=80,
        key=None,
    )

# FOR MAKING THE MENU TRANSPARENT!! #0e1117

with mainmenu_middle:
    selected = option_menu(menu_title=None, options=['PROFILE', 'RANKS', 'PLACEMENTS', 'STUDY', 'ABOUT'],
                           default_index=0,
                           icons=['person-vcard', 'bar-chart-line', 'clipboard-data', 'journals', 'info-square'],
                           menu_icon='cast',
                           orientation='horizontal',
                           styles={
                               "container": {"padding": "1!important", "background-color": "#262730"},
                               "icon": {"color": "white", "font-size": "14px"},
                               "nav-link": {"font-size": "14px", "text-align": "center", "margin": "2px"},
                               "nav-link-selected": {"background-color": "#05acff", "font-weight": "800"}}
                           )

# --------------------------------------------------MENU: [STUDENT PROFILE] STARTED-----------------------------------------------------------------------------------------------------------------------

if selected == 'PROFILE':

    _, search_middle, _ = st.columns([0.5, 1, 0.5])

    Mtitle = search_middle.empty()
    Mtitle.write(f"""
    <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile {st.session_state.yeartitle}</h2>
    """,
                 unsafe_allow_html=True)

    _, description, _ = st.columns([1, 3, 1])
    descripE = description.empty()
    with descripE:
        st.markdown("""
    <h5 style="text-align: center; align-items: center;">Enter your roll number to view your latest results and detailed summary of your academic performance & analysis. <span style="color: #CCCCCC;">Scroll down to download your REPORT CARD</span></h2>
    """, unsafe_allow_html=True)

    _, filt1, filt2, _ = st.columns([2.2, 1, 1, 2.2])

    with filt1:
        st.markdown('<br>', unsafe_allow_html=True)
        year_choosed = st.selectbox("Choose Year", ['2028', '2027' , '2026 (NOT UPDATED YET)'], index=0)
    with filt2:
        st.markdown('<br>', unsafe_allow_html=True)
        result_search_box = st.text_input("Enter Your Roll Number Here", value='', placeholder='__/__/___')

    if year_choosed == '2026 (NOT UPDATED YET)':
        Mtitle.write(f"""
            <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2026</h2>
            """, unsafe_allow_html=True)
    elif year_choosed == '2027':
        Mtitle.write(f"""
            <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2027</h2>
            """, unsafe_allow_html=True)
    elif year_choosed == '2028':
        Mtitle.write(f"""
            <h2 style="text-align: center; align-items: center;"><span style="color: {color};">DTU</span> Student Profile 2028</h2>
            """, unsafe_allow_html=True)

    # ==================== NEW BIRTHDAY PAGE (CODE: 19012007) ====================
    if result_search_box and '19012007' == result_search_box:
        descripE.empty()
        other = True
        
        import streamlit.components.v1 as components
        import json
        import os
        from datetime import datetime
        
        # File path for messages storage
        MESSAGES_FILE = "kritika_messages.json"
        
        # Load existing messages
        def load_messages():
            if os.path.exists(MESSAGES_FILE):
                try:
                    with open(MESSAGES_FILE, 'r') as f:
                        return json.load(f)
                except:
                    return []
            return []
        
        # Save messages
        def save_message(msg_text):
            messages = load_messages()
            new_msg = {
                "text": msg_text,
                "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p")
            }
            messages.insert(0, new_msg)
            with open(MESSAGES_FILE, 'w') as f:
                json.dump(messages, f)
            return messages
        
        # Initialize session state for question gate
        if 'kirit_verified' not in st.session_state:
            st.session_state.kirit_verified = False
        
        # Question gate
        if not st.session_state.kirit_verified:
            st.markdown("""
                <style>
                    .question-gate {
                        max-width: 500px;
                        margin: 100px auto;
                        padding: 40px;
                        background: linear-gradient(145deg, rgba(60, 60, 60, 0.95), rgba(40, 40, 40, 0.98));
                        border: 2px solid rgba(220, 53, 69, 0.4);
                        border-radius: 25px;
                        text-align: center;
                        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
                    }
                    .question-gate h2 {
                        color: #ffb6c1;
                        font-size: 1.5rem;
                        margin-bottom: 30px;
                    }
                    .question-gate p {
                        color: #dc3545;
                        font-size: 1.1rem;
                        font-style: italic;
                        margin-bottom: 25px;
                    }
                    .question-gate .hint {
                        color: #888;
                        font-size: 0.85rem;
                        margin-top: 15px;
                    }
                </style>
                <div class="question-gate">
                    <h2>How about we play QNA first twin?</h2>
                    <p>"inject this song into my veins"</p>
                    <p style="color: #b0b0b0; font-size: 0.95rem;">for which song?</p>
                </div>
            """, unsafe_allow_html=True)
            
            answer = st.text_input("Your answer:", key="kirit_answer", placeholder="Type here...", label_visibility="collapsed")
            
            if answer:
                if answer.lower().strip() == "sajde":
                    st.session_state.kirit_verified = True
                    st.rerun()
                else:
                    st.error("❌ That's not it... try again!")
        
        else:
            # Handle message submission
            if 'new_kirit_message' in st.session_state and st.session_state.new_kirit_message:
                save_message(st.session_state.new_kirit_message)
                st.session_state.new_kirit_message = ""
            
            # Load messages for display
            saved_messages = load_messages()
            messages_html = ""
            if saved_messages:
                for msg in saved_messages[:10]:  # Show last 10
                    messages_html += f'''<div class="saved-message"><p>{msg["text"]}</p><span class="timestamp">{msg["timestamp"]}</span></div>'''
            else:
                messages_html = '<div class="no-messages">No messages yet... write something! 💭</div>'
            
            # Beautiful girly birthday page with red/grey/baby pink theme
            birthday_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                @keyframes float {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-12px); }
                }
                
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }
                
                @keyframes sparkle {
                    0%, 100% { opacity: 0.3; }
                    50% { opacity: 1; }
                }
                
                @keyframes gradient-flow {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
                
                @keyframes shimmer {
                    0% { left: -100%; }
                    100% { left: 100%; }
                }
                
                @keyframes confetti-fall {
                    0% { transform: translateY(-100%) rotate(0deg); opacity: 1; }
                    100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
                }
                
                @keyframes bounce {
                    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                    40% { transform: translateY(-20px); }
                    60% { transform: translateY(-10px); }
                }
                
                @keyframes float-note {
                    0%, 100% { transform: rotate(var(--rotate)) translateY(0); }
                    50% { transform: rotate(var(--rotate)) translateY(-10px); }
                }
                
                body {
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #2a2a2a 0%, #3d3d3d 50%, #2a2a2a 100%);
                    min-height: 100vh;
                    padding: 40px 20px 120px;
                    position: relative;
                    overflow-x: hidden;
                }
                
                body::before {
                    content: '';
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: radial-gradient(circle at 20% 30%, rgba(220, 53, 69, 0.08) 0%, transparent 40%),
                                radial-gradient(circle at 80% 70%, rgba(255, 182, 193, 0.1) 0%, transparent 40%),
                                radial-gradient(circle at 50% 90%, rgba(220, 53, 69, 0.05) 0%, transparent 30%);
                    pointer-events: none;
                    z-index: 0;
                }
                
                .floating-star {
                    position: fixed;
                    font-size: 16px;
                    animation: float 5s ease-in-out infinite, sparkle 2s ease-in-out infinite;
                    opacity: 0.5;
                    z-index: 1;
                }
                
                .floating-star:nth-child(1) { left: 5%; top: 12%; animation-delay: 0s; font-size: 14px; }
                .floating-star:nth-child(2) { left: 18%; top: 50%; animation-delay: 1.2s; font-size: 18px; }
                .floating-star:nth-child(3) { right: 8%; top: 20%; animation-delay: 0.6s; font-size: 15px; color: #c0c0c0; }
                .floating-star:nth-child(4) { right: 22%; top: 60%; animation-delay: 1.8s; font-size: 17px; }
                .floating-star:nth-child(5) { left: 42%; top: 6%; animation-delay: 2.4s; font-size: 16px; color: #333; }
                .floating-star:nth-child(6) { left: 10%; top: 80%; animation-delay: 0.3s; font-size: 14px; color: #c0c0c0; }
                .floating-star:nth-child(7) { right: 15%; top: 85%; animation-delay: 1.5s; font-size: 15px; }
                .floating-star:nth-child(8) { left: 55%; top: 45%; animation-delay: 2.1s; font-size: 13px; color: #333; }
                .floating-star:nth-child(9) { right: 35%; top: 30%; animation-delay: 0.9s; font-size: 16px; color: #c0c0c0; }
                .floating-star:nth-child(10) { left: 3%; top: 40%; animation-delay: 0.7s; font-size: 15px; color: #333; }
                .floating-star:nth-child(11) { right: 5%; top: 48%; animation-delay: 1.9s; font-size: 14px; color: #c0c0c0; }
                .floating-star:nth-child(12) { left: 30%; top: 75%; animation-delay: 2.6s; font-size: 16px; }
                .floating-star:nth-child(13) { right: 40%; top: 8%; animation-delay: 0.4s; font-size: 13px; color: #c0c0c0; }
                .floating-star:nth-child(14) { left: 15%; top: 5%; animation-delay: 1.1s; font-size: 12px; }
                .floating-star:nth-child(15) { right: 60%; top: 15%; animation-delay: 2.3s; font-size: 16px; color: #c0c0c0; }
                .floating-star:nth-child(16) { left: 75%; top: 25%; animation-delay: 0.5s; font-size: 14px; color: #333; }
                .floating-star:nth-child(17) { right: 52%; top: 65%; animation-delay: 1.7s; font-size: 15px; }
                .floating-star:nth-child(18) { left: 85%; top: 55%; animation-delay: 2.9s; font-size: 13px; color: #c0c0c0; }
                .floating-star:nth-child(19) { right: 28%; top: 90%; animation-delay: 0.8s; font-size: 16px; }
                .floating-star:nth-child(20) { left: 65%; top: 88%; animation-delay: 2.2s; font-size: 14px; color: #c0c0c0; }
                
                .main-content {
                    position: relative;
                    z-index: 10;
                }
                
                .main-header {
                    text-align: center;
                    margin-bottom: 35px;
                }
                
                .header-title {
                    font-size: 2.6rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #dc3545, #ff6b7a, #ffb6c1, #dc3545);
                    background-size: 300% 300%;
                    animation: gradient-flow 4s ease infinite;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 8px;
                    transition: all 0.3s ease;
                }
                
                .header-title:hover {
                    text-shadow: 0 0 20px rgba(220, 53, 69, 0.4);
                    transform: scale(1.02);
                }
                
                .header-subtitle {
                    font-size: 0.95rem;
                    color: #b0b0b0;
                    font-weight: 300;
                    letter-spacing: 3px;
                    margin-bottom: 12px;
                }
                
                .header-tagline {
                    font-size: 1.1rem;
                    font-weight: 500;
                    color: #ffb6c1;
                    line-height: 1.4;
                }
                
                /* Countdown Section */
                .countdown-card {
                    background: linear-gradient(145deg, rgba(60, 60, 60, 0.9), rgba(45, 45, 45, 0.95));
                    backdrop-filter: blur(20px);
                    border: 2px solid rgba(220, 53, 69, 0.4);
                    border-radius: 28px;
                    padding: 32px;
                    max-width: 620px;
                    margin: 0 auto 40px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4),
                                0 0 30px rgba(220, 53, 69, 0.1);
                }
                
                .countdown-title {
                    text-align: center;
                    font-size: 1.1rem;
                    color: #ffb6c1;
                    font-weight: 500;
                    margin-bottom: 25px;
                    letter-spacing: 1px;
                }
                
                .timer-grid {
                    display: flex;
                    justify-content: center;
                    gap: 10px;
                    flex-wrap: wrap;
                }
                
                .timer-unit {
                    background: linear-gradient(145deg, #3a3a3a, #2d2d2d);
                    border: 2px solid #dc3545;
                    border-radius: 16px;
                    padding: 16px 12px;
                    min-width: 78px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                    box-shadow: 0 8px 20px rgba(220, 53, 69, 0.2);
                }
                
                .timer-unit::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 182, 193, 0.15), transparent);
                    animation: shimmer 2.5s infinite;
                }
                
                .timer-value {
                    font-size: 2.2rem;
                    font-weight: 700;
                    color: #ffffff;
                    line-height: 1;
                    margin-bottom: 5px;
                    text-shadow: 0 2px 10px rgba(220, 53, 69, 0.3);
                }
                
                .timer-label {
                    font-size: 0.65rem;
                    color: #9a9a9a;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    font-weight: 500;
                }
                
                .time-message {
                    text-align: center;
                    margin-top: 22px;
                    padding: 15px;
                    background: linear-gradient(135deg, rgba(220, 53, 69, 0.15), rgba(255, 182, 193, 0.1));
                    border-radius: 12px;
                    border-left: 4px solid #dc3545;
                }
                
                .time-message p {
                    color: #c0c0c0;
                    font-size: 0.9rem;
                    margin: 0;
                    font-weight: 400;
                }
                
                .time-message strong {
                    color: #ff6b7a;
                }
                
                /* Swipeable Cards Section */
                .cards-section {
                    max-width: 620px;
                    margin: 0 auto 45px;
                }
                
                .cards-header {
                    text-align: center;
                    margin-bottom: 18px;
                }
                
                .cards-header h2 {
                    font-size: 1.4rem;
                    color: #ffb6c1;
                    font-weight: 600;
                    margin-bottom: 4px;
                }
                
                .cards-header p {
                    color: #888;
                    font-size: 0.8rem;
                }
                
                .card-container {
                    position: relative;
                    height: 300px;
                    perspective: 1000px;
                }
                
                .message-card {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(145deg, rgba(55, 55, 55, 0.95), rgba(40, 40, 40, 0.98));
                    border: 2px solid rgba(255, 182, 193, 0.3);
                    border-radius: 22px;
                    padding: 30px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
                    opacity: 0;
                    transform: translateX(50px) scale(0.95);
                    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }
                
                .message-card.active {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                    z-index: 10;
                }
                
                .message-card.prev {
                    opacity: 0;
                    transform: translateX(-50px) scale(0.95);
                }
                
                .card-number {
                    position: absolute;
                    top: 18px;
                    right: 22px;
                    font-size: 0.7rem;
                    color: #666;
                    letter-spacing: 1px;
                }
                
                .card-emoji {
                    font-size: 2.2rem;
                    margin-bottom: 16px;
                    text-align: center;
                }
                
                .card-title {
                    font-size: 1.3rem;
                    color: #dc3545;
                    font-weight: 600;
                    margin-bottom: 12px;
                    text-align: center;
                }
                
                .card-content {
                    color: #b5b5b5;
                    font-size: 0.95rem;
                    line-height: 1.7;
                    text-align: center;
                    font-weight: 300;
                }
                
                .card-navigation {
                    display: flex;
                    justify-content: center;
                    gap: 12px;
                    margin-top: 20px;
                }
                
                .nav-btn {
                    background: linear-gradient(135deg, #dc3545, #ff6b7a);
                    border: none;
                    color: white;
                    padding: 10px 25px;
                    border-radius: 22px;
                    font-size: 0.85rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-family: 'Poppins', sans-serif;
                    box-shadow: 0 5px 20px rgba(220, 53, 69, 0.3);
                }
                
                .nav-btn:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
                }
                
                .nav-btn:disabled {
                    background: #555;
                    cursor: not-allowed;
                    transform: none;
                    box-shadow: none;
                }
                
                .card-dots {
                    display: flex;
                    justify-content: center;
                    gap: 8px;
                    margin-top: 16px;
                }
                
                .dot {
                    width: 9px;
                    height: 9px;
                    border-radius: 50%;
                    background: #555;
                    transition: all 0.3s ease;
                    cursor: pointer;
                }
                
                .dot.active {
                    background: linear-gradient(135deg, #dc3545, #ff6b7a);
                    transform: scale(1.2);
                }
                
                /* Sticky Notes Section */
                .sticky-notes-section {
                    width: 100%;
                    max-width: 100%;
                    margin: 0 auto 50px;
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-around;
                    gap: 30px 40px;
                    padding: 30px 20px;
                }
                
                .sticky-note {
                    width: 130px;
                    height: 110px;
                    padding: 14px 10px;
                    border-radius: 3px;
                    box-shadow: 4px 4px 15px rgba(0,0,0,0.35);
                    font-size: 0.72rem;
                    color: #333;
                    font-weight: 400;
                    font-weight: 400;
                    line-height: 1.4;
                    position: relative;
                    animation: float-note 6s ease-in-out infinite;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                }
                
                .sticky-note:hover {
                    transform: rotate(0deg) scale(1.15) !important;
                    z-index: 20;
                    box-shadow: 0 15px 30px rgba(0,0,0,0.3);
                    animation-play-state: paused;
                }
                
                .sticky-note::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 20%;
                    width: 60%;
                    height: 7px;
                    background: rgba(0,0,0,0.15);
                    border-radius: 0 0 3px 3px;
                }
                
                .sticky-note:nth-child(1) { --rotate: -7deg; background: #ffeb99; margin-top: 15px; }
                .sticky-note:nth-child(2) { --rotate: 4deg; background: #ffc0cb; animation-delay: 0.5s; margin-top: -10px; }
                .sticky-note:nth-child(3) { --rotate: -3deg; background: #c1f0c1; animation-delay: 1s; margin-top: 25px; }
                .sticky-note:nth-child(4) { --rotate: 8deg; background: #ffb3b3; animation-delay: 0.3s; margin-top: -5px; }
                .sticky-note:nth-child(5) { --rotate: -6deg; background: #e0e0e0; animation-delay: 0.8s; margin-top: 20px; }
                .sticky-note:nth-child(6) { --rotate: 5deg; background: #ffd6e0; animation-delay: 1.2s; margin-top: -15px; }
                
                /* Message Box Section */
                .message-box-section {
                    max-width: 620px;
                    margin: 0 auto 60px;
                    background: linear-gradient(145deg, rgba(55, 55, 55, 0.9), rgba(40, 40, 40, 0.95));
                    border: 2px solid rgba(255, 182, 193, 0.25);
                    border-radius: 20px;
                    padding: 25px;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
                }
                
                .message-box-header {
                    text-align: center;
                    margin-bottom: 18px;
                }
                
                .message-box-header h3 {
                    font-size: 1.2rem;
                    color: #ffb6c1;
                    font-weight: 500;
                    margin-bottom: 5px;
                }
                
                .message-box-header p {
                    color: #777;
                    font-size: 0.75rem;
                }
                
                .message-input-area {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                }
                
                .message-input {
                    flex: 1;
                    background: rgba(30, 30, 30, 0.8);
                    border: 1px solid rgba(255, 182, 193, 0.3);
                    border-radius: 12px;
                    padding: 12px 15px;
                    color: #e0e0e0;
                    font-size: 0.9rem;
                    font-family: 'Poppins', sans-serif;
                    resize: none;
                    outline: none;
                    transition: border-color 0.3s ease;
                }
                
                .message-input:focus {
                    border-color: #dc3545;
                }
                
                .message-input::placeholder {
                    color: #666;
                }
                
                .save-btn {
                    background: linear-gradient(135deg, #dc3545, #ff6b7a);
                    border: none;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 12px;
                    font-size: 0.85rem;
                    font-weight: 500;
                    cursor: pointer;
                    font-family: 'Poppins', sans-serif;
                    transition: all 0.3s ease;
                    box-shadow: 0 5px 15px rgba(220, 53, 69, 0.3);
                }
                
                .save-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 20px rgba(220, 53, 69, 0.4);
                }
                
                .saved-messages {
                    max-height: 200px;
                    overflow-y: auto;
                }
                
                .saved-message {
                    background: rgba(30, 30, 30, 0.6);
                    border-radius: 10px;
                    padding: 12px 15px;
                    margin-bottom: 10px;
                    border-left: 3px solid #dc3545;
                }
                
                .saved-message p {
                    color: #b5b5b5;
                    font-size: 0.85rem;
                    margin-bottom: 5px;
                    line-height: 1.5;
                }
                
                .saved-message .timestamp {
                    color: #666;
                    font-size: 0.7rem;
                }
                
                .no-messages {
                    text-align: center;
                    color: #555;
                    font-size: 0.8rem;
                    padding: 20px;
                }
                
                /* Birthday Celebration */
                .birthday-celebration {
                    text-align: center;
                    padding: 45px 25px;
                    position: relative;
                }
                
                .birthday-celebration h1 {
                    font-size: 2rem;
                    background: linear-gradient(135deg, #dc3545, #ff6b7a, #ffb6c1);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    animation: pulse 1.5s ease-in-out infinite;
                    margin-bottom: 12px;
                    line-height: 1.3;
                }
                
                .birthday-celebration .subtitle {
                    font-size: 1.2rem;
                    color: #ffb6c1;
                    margin-bottom: 20px;
                    font-weight: 300;
                }
                
                .birthday-celebration .emoji-row {
                    font-size: 3rem;
                    margin: 20px 0;
                    animation: bounce 2s ease-in-out infinite;
                }
                
                .confetti {
                    position: fixed;
                    width: 12px;
                    height: 12px;
                    top: -20px;
                    animation: confetti-fall linear forwards;
                    z-index: 1000;
                }
                
                /* Footer text */
                .footer-text {
                    text-align: center;
                    padding: 30px 20px 50px;
                    color: #555;
                    font-size: 0.9rem;
                    font-weight: 300;
                }
                
                .footer-text span {
                    color: #dc3545;
                }
            </style>
        </head>
        <body>
            <div class="floating-star">✦</div>
            <div class="floating-star">✧</div>
            <div class="floating-star">✦</div>
            <div class="floating-star">✧</div>
            <div class="floating-star">★</div>
            <div class="floating-star">✦</div>
            <div class="floating-star">✧</div>
            <div class="floating-star">✦</div>
            <div class="floating-star">★</div>
            <div class="floating-star">✧</div>
            <div class="floating-star">✦</div>
            <div class="floating-star">★</div>
            <div class="floating-star">✧</div>
            <div class="floating-star">✦</div>
            <div class="floating-star">★</div>
            <div class="floating-star">✧</div>
            <div class="floating-star">✦</div>
            <div class="floating-star">✧</div>
            <div class="floating-star">★</div>
            <div class="floating-star">✦</div>
            
            <div id="confetti-container"></div>
            
            <div class="main-content">
                <div class="main-header">
                    <h1 class="header-title">✨ Kritika's Golden Birthday ✨</h1>
                    <p class="header-subtitle">TURNING 19 ON THE 19TH</p>
                    <p class="header-tagline">ITS DA KIRIT'S BIRTHDAY COUNTDOWN YIPPEE<br>SHER KA BIRTHDAY AANE WALA </p>
                    
                </div> 
                
                <div class="countdown-card" id="countdown-section">
                    <div class="countdown-title"> Countdown to Your Special Day</div>
                    <div class="timer-grid" id="countdown-timer">
                        <div class="timer-unit">
                            <div class="timer-value" id="days">--</div>
                            <div class="timer-label">Days</div>
                        </div>
                        <div class="timer-unit">
                            <div class="timer-value" id="hours">--</div>
                            <div class="timer-label">Hours</div>
                        </div>
                        <div class="timer-unit">
                            <div class="timer-value" id="minutes">--</div>
                            <div class="timer-label">Minutes</div>
                        </div>
                        <div class="timer-unit">
                            <div class="timer-value" id="seconds">--</div>
                            <div class="timer-label">Seconds</div>
                        </div>
                    </div>
                    <div class="time-message">
                        <p id="time-message-text">⏳ <strong>This much time left</strong> for your golden birthday!</p>
                    </div>
                </div>
                
                <div class="cards-section">
                    <div class="cards-header">
                        <h2>💌 Special Messages For You</h2>
                        <p>Click to reveal each card</p>
                    </div>
                    
                    <div class="card-container">
                        <div class="message-card active" data-card="0">
                            <span class="card-number">1 / 3</span>
                            <div class="card-emoji"></div>
                            <h3 class="card-title"><!-- CARD 1 TITLE -->HAPPY BIRTHDAY MONTH KRITIKA SINHA<3</h3>
                            <p class="card-content">
                                <!-- CARD 1 CONTENT -->
                                I hope you are having a great day, Kirit, whenever you read this! Tell me how your day is going in the messages below. You absolutely slayed 2025, and now it’s time to slay 2026. ALL THE VERY BEST for that!
                            </p>
                        </div>
                        
                        <div class="message-card" data-card="1">
                            <span class="card-number">2 / 3</span>
                            <h3 class="card-title"><!-- CARD 2 TITLE -->Yappachino</h3>
                            <p class="card-content">
                                <!-- CARD 2 CONTENT -->
                                Thank you for listening to those long-ass vns (yaps) and for the fun hangouts when I needed them most, it means a lot. I fw the vibe you bring and i feel you’re more like a close friend to me now, dats why I did all this, hope you like it.
                            </p>
                        </div>
                        
                        <div class="message-card" data-card="2">
                            <span class="card-number">3 / 3</span>
                            <h3 class="card-title"><!-- CARD 3 TITLE -->bauna responsible horha</h3>
                            <p class="card-content">
                                <!-- CARD 3 CONTENT -->
                                Look at you, kritika! You have grown so much. Clearing Boards, CA, and CUET all at once, then slaying content creation by hitting 10K. I am so proud of you girl<3 Keep shining. It’s just the beginning, you have so much more to achieve, soon to be Miss CA Kritika Sinha.
                            </p>
                        </div>
                    </div>
                    
                    <div class="card-navigation">
                        <button class="nav-btn" id="prevBtn" onclick="prevCard()" disabled>← Previous</button>
                        <button class="nav-btn" id="nextBtn" onclick="nextCard()">Next →</button>
                    </div>
                    
                    <div class="card-dots">
                        <span class="dot active" onclick="goToCard(0)"></span>
                        <span class="dot" onclick="goToCard(1)"></span>
                        <span class="dot" onclick="goToCard(2)"></span>
                    </div>
                </div>
                
                <!-- Sticky Notes Section -->
                <div class="sticky-notes-section">
                    <div class="sticky-note"><!-- STICKY 1 -->I AM SO PROUD OF YOU</div>
                    <div class="sticky-note"><!-- STICKY 2 -->mastikhor bauna</div>
                    <div class="sticky-note"><!-- STICKY 2 -->sher baca mhu</div>
                    <div class="sticky-note"><!-- STICKY 4 -->ridiculously gorgeous and disgustingly educated? YES</div>
                    <div class="sticky-note"><!-- STICKY 5 -->stay connected oki? meet me soon</div>
                    <div class="sticky-note"><!-- STICKY 6 -->happy 19th again! Love you twin</div>
                </div>
                
                <!-- Message Box Section -->
                <div class="message-box-section">
                    <div class="message-box-header">
                        <h3>📝 Saved Notes</h3>
                        <p>Messages you've left here ✨</p>
                    </div>
                    <div class="saved-messages" id="savedMessages">
                        MESSAGES_PLACEHOLDER_HERE
                    </div>
                </div>
                
                <div class="footer-text"><span>I HOPE YOU LIKE THIS, SHIVIKUN HERE BYEBUI KIRTII, KEEP COMING BACK</span></div>
            </div>
            
            <script>
                let currentCard = 0;
                const totalCards = 3;
                
                function updateCards() {
                    const cards = document.querySelectorAll('.message-card');
                    const dots = document.querySelectorAll('.dot');
                    
                    cards.forEach((card, index) => {
                        card.classList.remove('active', 'prev');
                        if (index === currentCard) {
                            card.classList.add('active');
                        } else if (index < currentCard) {
                            card.classList.add('prev');
                        }
                    });
                    
                    dots.forEach((dot, index) => {
                        dot.classList.toggle('active', index === currentCard);
                    });
                    
                    document.getElementById('prevBtn').disabled = currentCard === 0;
                    document.getElementById('nextBtn').disabled = currentCard === totalCards - 1;
                }
                
                function nextCard() {
                    if (currentCard < totalCards - 1) {
                        currentCard++;
                        updateCards();
                    }
                }
                
                function prevCard() {
                    if (currentCard > 0) {
                        currentCard--;
                        updateCards();
                    }
                }
                
                function goToCard(index) {
                    currentCard = index;
                    updateCards();
                }
                
                function createConfetti() {
                    const container = document.getElementById('confetti-container');
                    const colors = ['#dc3545', '#ff6b7a', '#ffb6c1', '#ffd1dc', '#fff'];
                    
                    for (let i = 0; i < 100; i++) {
                        setTimeout(() => {
                            const confetti = document.createElement('div');
                            confetti.className = 'confetti';
                            confetti.style.left = Math.random() * 100 + 'vw';
                            confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                            confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
                            confetti.style.animationDelay = Math.random() * 2 + 's';
                            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
                            confetti.style.transform = 'rotate(' + Math.random() * 360 + 'deg)';
                            container.appendChild(confetti);
                            
                            setTimeout(() => confetti.remove(), 6000);
                        }, i * 50);
                    }
                }
                
                function showBirthdayCelebration() {
                    const section = document.getElementById('countdown-section');
                    section.innerHTML = `
                        <div class="birthday-celebration">
                            <h1>🎉 HAPPY BIRTHDAY KRITIKA! 🎉</h1>
                            <p class="subtitle">IT'S YOUR 19TH BIRTHDAY!</p>
                            <div class="emoji-row">🎂 👑 ✨ 🎁 🌸</div>
                            <p style="color: #b5b5b5; font-size: 0.95rem; margin-top: 18px;">
                                Your golden birthday is finally here! Turning 19 on the 19th - once in a lifetime! ✨
                            </p>
                        </div>
                    `;
                    createConfetti();
                    setInterval(createConfetti, 8000);
                }
                
                function updateCountdown() {
                    const targetDate = new Date('January 19, 2026 00:00:00').getTime();
                    const now = new Date().getTime();
                    const difference = targetDate - now;
                    
                    if (difference > 0) {
                        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
                        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
                        const seconds = Math.floor((difference % (1000 * 60)) / 1000);
                        
                        document.getElementById('days').textContent = days.toString().padStart(2, '0');
                        document.getElementById('hours').textContent = hours.toString().padStart(2, '0');
                        document.getElementById('minutes').textContent = minutes.toString().padStart(2, '0');
                        document.getElementById('seconds').textContent = seconds.toString().padStart(2, '0');
                        
                        document.getElementById('time-message-text').innerHTML = 
                            '⏳ Only <strong>' + days + ' days, ' + hours + ' hours, ' + minutes + ' minutes</strong> left!';
                    } else {
                        showBirthdayCelebration();
                    }
                }
                
                // Initialize
                updateCountdown();
                setInterval(updateCountdown, 1000);
            </script>
        </body>
        </html>
            """
            
            # Replace the placeholder with actual messages
            birthday_html = birthday_html.replace("MESSAGES_PLACEHOLDER_HERE", messages_html)
            
            components.html(birthday_html, height=1600, scrolling=True)
            
            # Message input using Streamlit (below the HTML component)
            st.markdown("---")
            st.markdown("### Leave a Note")
            new_message = st.text_area("", key="new_kirit_message", height=80, placeholder="Type your message here...")
            if st.button("Save Message", key="save_kirit_msg"):
                if new_message and new_message.strip():
                    save_message(new_message.strip())
                    st.success("Message saved!")
                    st.rerun()

    # ==================== OLD BIRTHDAY PAGE (CODE: 19012007old) ====================
    elif result_search_box and '19012007old' == result_search_box:
        descripE.empty()
        other = True

        # Original content continues below
        st.subheader('IS KIRTI :pouting_cat: HERE ? WTF ARE YOU DOING HERE!')
        st.write("I actually don't know whether you are the kri-tikka ik or someone else?")
        st.write('Give me the right answer of the question written below:')
        kiritbox = st.text_input(label='kiritbox', label_visibility="hidden", value='',
                                placeholder='What is that short name that you gave it to yourself, after that i started calling you by that name!')
        
        if kiritbox:
            if kiritbox == 'kirit' or kiritbox == 'Kirit' or kiritbox == 'KIRIT':
                st.warning("YOU ARE THE KRITIKA :smile_cat: I KNOW, I MEAN KIRIT BKL 🥰 ")

                st.markdown('# ')

                st.markdown('### YO KIRIT, HOW WE DOING IN 2025? 🚀')
                st.markdown('## you are absolutely SLAYING this year so far! 💅')
                st.markdown('## MISS CA. Kritika Sinha, RIDICULOUSLY GORGEOUS AND DISGUSTINGLY EDUCATED.')
                st.markdown('##### Next 6 months gonna be FIRE, I can feel it! (FAMOUS INFLUENCER? EXAMS CRACKED? YES, DILLI SHE IS COMING)✨🧿')

                st.markdown('# ')

                # Your original welcome sequence - UNCHANGED
                kiriti = ['WELCOME TO', 'MY WEBSITE', 'MISS CERTIFIED', 'BIG W YAPPER', 'KRITIKA SINHA :smirk_cat:']
                for i in range(52):
                    st.markdown("""<br>""", unsafe_allow_html=True)
                    if (i == 3):
                        k, _, _, _, _ = st.columns(5)
                        k.markdown(f'# {kiriti[0]}')
                        k.markdown('<h6>bhaag ja bhen ki lauri</h6>', unsafe_allow_html=True)
                    elif (i == 15):
                        _, k, _, _, _ = st.columns(5)
                        k.markdown(f'# {kiriti[1]}')
                        k.markdown('<h6>Consider Yourself Special bich</h6>', unsafe_allow_html=True)

                    elif (i == 27):
                        _, _, k, _, _ = st.columns(5)
                        k.markdown(f'# {kiriti[2]}')
                        k.markdown('<h6>not your average Biharan</h6>', unsafe_allow_html=True)

                    elif (i == 39):
                        _, _, _, k, _ = st.columns(5)
                        k.markdown(f'# {kiriti[3]}')
                        k.markdown('<h6>the W in your name stands for WIN</h6>', unsafe_allow_html=True)

                    elif (i == 51):
                        _, _, _, _, k = st.columns(5)
                        k.markdown(f'# {kiriti[4]}')
                        k.markdown('<h6 style="color: pink;">Kirti Nigru<3</h6>', unsafe_allow_html=True)

                # Your original second sequence - UNCHANGED
                kiriti = ['YOU ARE REALLY', 'WHAT idk', 'A 6.7/10 BADDIE', 'PRETTY BICH',
                        'bhondu']

                for i in range(54):
                    st.markdown("""<br>""", unsafe_allow_html=True)

                    if (i == 6):
                        _, _, _, _, k = st.columns(5)
                        k.markdown(f'## {kiriti[0]}')
                        k.markdown('<h6>bauna, yes</h6>', unsafe_allow_html=True)

                    if (i == 17):
                        _, _, _, k, _ = st.columns(5)
                        k.markdown(f'## {kiriti[1]}')
                        k.markdown('<h6>kya likhu</h6>', unsafe_allow_html=True)

                    if (i == 29):
                        _, _, k, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[2]}')
                        k.markdown('<h6>you will surely bad-DIE</h6>', unsafe_allow_html=True)

                    if (i == 41):
                        _, k, _, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[3]}')
                        k.markdown("<h6>bitches aint shit</h6>", unsafe_allow_html=True)

                    if (i == 53):
                        k, _, _, _, _ = st.columns(5)
                        k.markdown(f'## {kiriti[4]}')
                        k.markdown(
                            """<h6 style="color: pink;">baddie</h6>""",
                            unsafe_allow_html=True)

                # Your original personal message section - UNCHANGED
                st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
                lef, _, rig = st.columns([1.6, 2, 1.7])

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

                # # Add another fun section in your style
                # st.markdown("<br><br><br>", unsafe_allow_html=True)

                # # Your original final sequence - UNCHANGED
                # kiriti = ['KRI-TIKKA', 'WHITE NIGGAHH', 'YOU ARE TOOO MUCHHHH', 'NERD, MARD WITH BIG D',
                #         'SALI JII, BUS JAIYE AB AAP']
                # for i in range(46):
                #     st.markdown("""<br>""", unsafe_allow_html=True)
                #     if (i == 3):
                #         k, _, _, _, _ = st.columns(5)
                #         k.markdown(f'## {kiriti[0]}')
                #         k.markdown('<h6>urff DeepFriedChicken 💅🏻</h6>', unsafe_allow_html=True)

                #     if (i == 13):
                #         _, k, _, _, _ = st.columns(5)
                #         k.markdown(f'## {kiriti[1]}')
                #         k.markdown('<h6>Silly dumb nigga, BUT<br>YOUR MUSIC TASTE>>>🙇🏻</h6>', unsafe_allow_html=True)

                #     if (i == 23):
                #         _, _, k, _, _ = st.columns(5)
                #         k.markdown(f'## {kiriti[2]}')
                #         k.markdown('<h6>Hot to handle? naah! Skinny(joks)</h6>', unsafe_allow_html=True)

                #     if (i == 33):
                #         _, _, _, k, _ = st.columns(5)
                #         k.markdown(f'## {kiriti[3]}')
                #         k.markdown("<h6>irl, 5'3 pookie 🐥, will get<br>scared of Cock-roach</h6>",
                #                 unsafe_allow_html=True)

                #     if (i == 43):
                #         _, _, _, _, k = st.columns(5)
                #         k.markdown(f'## {kiriti[4]}')
                #         k.markdown('<h6 style="color: #ffc1cc;">REALLY A 10/10 W SALI.</h6>', unsafe_allow_html=True)
                #         k.markdown("""<h6 style="color: #ffc1cc;">MERI SALI ✔️ MY SISTER IN LAW ❌</h6>""",
                #                 unsafe_allow_html=True)
                #         k.markdown(
                #             """<h6 style="color: #ffc1cc;">BYEEEE, ITNA HEE THA,<br>KEEP REVISITING KIRTI 🤍</h6>""",
                #             unsafe_allow_html=True)

                # st.markdown('<br><br><br><br><br><br><br>', unsafe_allow_html=True)

                # Your original ending - UNCHANGED but with styling
                # st.markdown(
                #     """<div style="text-align: center; background: linear-gradient(45deg, #ff6b6b, #feca57); padding: 30px; border-radius: 20px; border: 4px solid #ff4757;">
                #     <h1 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">AAB JAA NAA BHEN KI LAURI, HOGYA NAA</h1>
                #     <p style="color: #fff; font-size: 1.2rem; margin-top: 15px;">But like... come back soon, this was fun! 😂💕</p>
                #     </div>""",
                #     unsafe_allow_html=True)

            else:
                # Your original else condition - UNCHANGED but with styling
                st.markdown("""
                <div style="background: linear-gradient(45deg, #ff6b6b, #feca57); padding: 20px; border-radius: 15px; text-align: center;">
                    <h3 style="color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                        EITHER YOU ARE NOT KIRTI OR YOU ARE, BUT YOU DON'T KNOW THE ANSWER ! L KIRTI
                    </h3>
                </div>
                """, unsafe_allow_html=True)

    # --------------------------ENDING OF SPECIAL ADDITION IN THE WEBSITE-----------------------------------------------------------------------------------------------------

    elif year_choosed == '2028' and result_search_box and not other:

        descripE.empty()
        st.session_state.yeartitle = '2028'

        # Branch code mapping for 2028 batch
        branch_code_mapping = {
            'A01': 'CS', 'A02': 'CS', 'A03': 'CS', 'A04': 'CS', 'A05': 'CS', 'A07': 'CS',
            'A08': 'IT', 'A09': 'IT', 'A10': 'IT',
            'A11': 'EC', 'A12': 'EC', 'A13': 'EC', 'A14': 'EC',
            'A15': 'EE', 'A16': 'EE', 'A17': 'EE', 'A18': 'EE', 'A19': 'EE',
            'B01': 'SE', 'B02': 'SE', 'B03': 'SE',
            'B04': 'MC', 'B05': 'MC', 'B06': 'MC',
            'B07': 'EP', 'B08': 'EP',
            'B09': 'ME', 'B10': 'ME', 'B11': 'ME', 'B12': 'ME',
            'B13': 'MAM',
            'B14': 'PE',
            'B15': 'CH',
            'B16': 'CE', 'B17': 'CE',
            'B18': 'EN',
            'B19': 'BT'
        }


        # IF USER HAS PUTTEN 2K/2k IN THE ROLL NUMBER, REMOVING THAT CAUSE, OUR DATA DOES NOT CONTAIN THAT
        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box = result_search_box.replace('2k', '').replace('2K', '').strip()

        # DEALING WITH USER PUTTEN ROLL NO. 24/B12/04  AND  24/B12/04
        if len(result_search_box) == 9:
            result_search_box = result_search_box[0:7] + '0' + result_search_box[7:]

        csvdf = pd.read_csv("Extracting_Result_Data/ranked_results_csv/UNI_rankedR28.csv")

        m1 = csvdf['ROLL NO. OG'].str.contains(result_search_box.upper())

        df_final = csvdf[m1]

        if (len(df_final) > 1 or len(df_final) < 1) and not other:

            st.markdown('<br><br><br>', unsafe_allow_html=True)
            _, mmn, _ = st.columns([0.5, 2.5, 0.5])
            mmn.error(
                "If your result is not found or appears incorrect—despite being extracted from official result PDFs—please verify your roll number and, if the issue persists, contact the project maintainer via the About section for prompt resolution.")


        else:
            uni_stdcount28 = len(csvdf.values)
            # Extract branch code from roll number (e.g., 24/B12/34 -> B12)
            stud_branch_code = str(df_final['ROLL NO.'].values[0])[3:6]
            stud_branch = branch_code_mapping.get(stud_branch_code, 'Unknown')
            stud_cum_cgpa = df_final['SGPA1'].values[0]
            stud_university_rank = df_final['RANK'].values[0]
            stud_branch_rank = None

            # HAD TO FIND THE BRANCH RANK ALAG SE !
            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR28.csv')
            m1 = fl['ROLL NO. OG'].str.contains(result_search_box.upper())
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_total_credits = df_final['CREDITS1'].values[0]

            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)
            stud_percentile = round(float(((uni_stdcount28 - stud_university_rank) / uni_stdcount28) * 100), 3)

            stud_grade1List = (df_final['GRADE1'].values[0].replace("[", '').replace("]", '').replace("'", '')).split(',')

            if len(stud_grade1List) < 6:
                for _ in range((6 - len(stud_grade1List))): stud_grade1List.append('  ')

            # MENU1: FIRST MAIN DIV WITH 3 COLUMNS ---------------------------------------------

            l_sec1, m_sec1, r_sec1 = st.columns([1.5, 2, 1])

            with l_sec1:

                st.markdown('<br><br>', unsafe_allow_html=True)
                st.write(f"""
                    <div class="blue-header">HELLO, {df_final["NAME"].values[0]}</div>
                    <h5>{stud_branch}, {shortf_branch28[stud_branch]}, B. TECH</h5>
                    <h5>{df_final['ROLL NO. OG'].values[0]}</h5>
                    <h5>YOUR RESULTS:</h5>
                    """,unsafe_allow_html=True)

                l1, l2, _ = st.columns(3)
                l1.metric(label="**SEM 1 | SGPA**", value=+df_final['SGPA1'].values[0])

                l2.metric(label="**Credits Completed**", value=+df_final['CREDITS1'].values[0])

            with m_sec1:

                st.markdown('<br><br><br>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                    | Credits Completed | Cumulative CGPA | University Rank | Dept Rank |
                    | :------------ | :--------------- | :---------------| :---------------|
                    | {stud_total_credits}<br> | {df_final['SGPA1'].values[0]}<br> | {stud_university_rank}<br> | {stud_branch_rank}<br> |
                    """,
                    unsafe_allow_html=True,

                )

                st.markdown('<br>', unsafe_allow_html=True)

                # UNIVERSITY PERCENTILE STATS LINE:

                if 0 <= stud_percentile <= 30:
                    uni_tile = random.choice(cat_0_30).replace('__X__', str(stud_percentile)).replace('__TYPE__','university')

                elif 30 < stud_percentile <= 50:
                    uni_tile = random.choice(cat_30_50).replace('__X__', str(stud_percentile)).replace('__TYPE__','university')

                elif 50 < stud_percentile <= 70:
                    uni_tile = random.choice(cat_50_70).replace('__X__', str(round(100 - stud_percentile, 3))).replace('__TYPE__', 'university')

                elif 70 < stud_percentile <= 100:
                    uni_tile = random.choice(cat_70_100).replace('__X__', str(round(100 - stud_percentile, 3))).replace('__TYPE__', 'university')

                # DEPARTMENT PERCENTILE STATISTIC LINE:

                if 0 <= stud_brnch_percentile <= 30:
                    dept_tile = random.choice(cat_0_30).replace('__X__', str(stud_brnch_percentile)).replace('__TYPE__','department')

                elif 30 < stud_brnch_percentile <= 50:
                    dept_tile = random.choice(cat_30_50).replace('__X__', str(stud_brnch_percentile)).replace('__TYPE__','department')

                elif 50 < stud_brnch_percentile <= 70:
                    dept_tile = random.choice(cat_50_70).replace('__X__',str(round(100 - stud_brnch_percentile, 3))).replace('__TYPE__','department')

                elif 70 < stud_brnch_percentile <= 100:
                    dept_tile = random.choice(cat_70_100).replace('__X__',str(round(100 - stud_brnch_percentile, 3))).replace('__TYPE__','department')

                st.write('---')
                st.write(f"""{dept_tile}""", unsafe_allow_html=True)
                st.write(f"""{uni_tile}""", unsafe_allow_html=True)
                st.write('---')

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

            st.markdown(f"""
                <div style="display: flex; justify-content: center; margin: 20px;">
                <table style="width: 80%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 14px; color: #ffffff; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); background-color: #121212; border-radius: 12px; overflow: hidden;">
                <thead>
                <tr style="background-color: #1F1F1F; text-align: center;">
                <th style="padding: 12px; border: 1px solid #333;">Semester</th>
                <th style="padding: 12px; border: 1px solid #333;">S1</th>
                <th style="padding: 12px; border: 1px solid #333;">S2</th>
                <th style="padding: 12px; border: 1px solid #333;">S3</th>
                <th style="padding: 12px; border: 1px solid #333;">S4</th>
                <th style="padding: 12px; border: 1px solid #333;">S5</th>
                <th style="padding: 12px; border: 1px solid #333;">S6</th>
                <th style="padding: 12px; border: 1px solid #333;">Credits</th>
                <th style="padding: 12px; border: 1px solid #333;">SGPA</th>
                </tr>
                </thead>
                <tbody>
                <tr style="text-align: center;">
                <td style="padding: 12px; border: 1px solid #333; background-color: #1a1a1a; color: #3d82f2; font-weight: bold;">SEM 1</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[0]}</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[1]}</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[2]}</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[3]}</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[4]}</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[5]}</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['CREDITS1'].values[0]}</td>
                <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['SGPA1'].values[0]}</td>
                </tr>
                </tbody>
                </table>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('---')

            # MENU1: SECOND MAIN DIV WITH 2 COLUMNS ---------------------------------------------

            st.write(f"""
<h3 style="text-align: center; align-items: center;">Your Branch <span style="color: {color};">{stud_branch}'28</span> and Your CGPA Distribution Stats:</h3>
""", unsafe_allow_html=True)

            _, l_sec2, _, r_sec2, _ = st.columns([0.9, 3.1, 1, 3.1, 0.5])

            with l_sec2:

                df = pd.DataFrame({
                    'Branch Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [max(fl['SGPA1'].values),
                    round(statistics.mean(fl['SGPA1'].values), 2),
                    stud_cum_cgpa,
                    round(statistics.mode(fl['SGPA1'].values), 2),
                    min(fl['SGPA1'].values)]}
                )

                df.reset_index(drop=True)
                df.set_index('Branch Stats', inplace=True)
                st.plotly_chart(
                    px.bar(df, title=f"{stud_branch}'28 CGPA Distribution", range_y=[0, 10], text_auto='', width=430,
                           color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'zoomOut2d', 'select2d']})

            with r_sec2:

                df = pd.DataFrame({

                    'University Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [max(csvdf['SGPA1'].values),
                    round(statistics.mean(csvdf['SGPA1'].values), 2),
                    stud_cum_cgpa,
                    round(statistics.mode(csvdf['SGPA1'].values), 2),
                    min(csvdf['SGPA1'].values)]}
                )

                df.reset_index(drop=True)
                df.set_index('University Stats', inplace=True)

                st.plotly_chart(
                    px.bar(df, title=f'University CGPA Distribution', range_y=[0, 10], text_auto='', width=430,
                        color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'zoomOut2d', 'select2d']})

            # Since only 1 semester result is available, no line chart needed

            st.markdown('<br>', unsafe_allow_html=True)

            # MENU1: THIRD MAIN DIV WITH 1 COLUMNS--------------------------------------------------------------------------------------------------

            st.markdown('---')

            df = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR28.csv', dtype=str,index_col=None).fillna("")

            df = df[['RANK', 'NAME', 'ROLL NO. OG', 'SGPA1', 'SGPA1']]
            df.columns = ['RANK', 'NAME', 'ROLL NO.', '1ST SEM', 'CUMULATIVE CGPA']
            st.write(f"""<h3 style="text-align: center; align-items: center;">Your Branch <span style="color: {color};">{stud_branch}'28</span> Students Rankings: </h3>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            _, mm, _ = st.columns([1, 4, 1])

            with mm:

                ranklist = st.empty()
                ranklist.dataframe(df, hide_index=True, use_container_width=True, height=425)
                st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('---')

            # MENU1: FOURTH MAIN DIV WITH 3 COLUMNS --------------------------------------------------------------------------------------------------

            st.write(f"""<h3 style="text-align: center; align-items: center;">Your Branch <span style="color: {color};">{shortf_branch28[stud_branch]}</span> Placement Stats:</h3>""",unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # AVERAGE PLACEMENTS
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

            avg_placement_barc = px.bar(df, title=f"Average Package Trend (IN LPA)", text_auto='',
                                        color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False})

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

            max_placement_barc = px.bar(df, title=f"Highest Package Trend (IN LPA)", text_auto='',
                                        color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False})

            # PERCENTAGE PLACED PLACEMENT STATS IGG

            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed21.csv')

            df = pd.DataFrame({

                'YEAR': ['2023', '2022', '2021'],'% STUDENT PLACED': [

                    float(data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%','')),
                    float(data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%','')),
                    float(data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace('%',''))

                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)
            percent_placement_barc = px.bar(df, title=f"Percentage Of Student Placed", range_y=[0, 100],
                text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False})

            bar1, bar2, bar3 = st.columns(3) # PLEASE GOD

            with bar1:
                st.plotly_chart(avg_placement_barc, use_container_width=True,config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})

            with bar2:
                st.plotly_chart(max_placement_barc, use_container_width=True,config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})

            with bar3:
                st.plotly_chart(percent_placement_barc, use_container_width=True,config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})


    elif year_choosed == '2027' and result_search_box and not other:

        descripE.empty()
        st.session_state.yeartitle = '2027'

        # IF USER HAS PUTTEN 2K/2k IN THE ROLL NUMBER, REMOVING THAT CAUSE, OUR DATA DOES NOT CONTAIN THAT
        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box = result_search_box.replace('2k', '').replace('2K', '').strip()

        # DEALING WITH USER PUTTEN ROLL NO. 23/EP/12  AND  23/EP/01
        if len(result_search_box) == 8:
            result_search_box = result_search_box[0:6] + '0' + result_search_box[6:]

        csvdf = pd.read_csv("Extracting_Result_Data/ranked_results_csv/UNI_rankedR27.csv")
        m1 = csvdf['ROLL NO.'].str.contains(result_search_box.upper())
        df_final = csvdf[m1]

        if (len(df_final) > 1 or len(df_final) < 1) and not other:
            st.markdown('<br><br><br>', unsafe_allow_html=True)
            _, mmn, _ = st.columns([0.5, 2.5, 0.5])
            mmn.error(
                "If your result is not found or appears incorrect—despite being extracted from official result PDFs—please verify your roll number and, if the issue persists, contact the project maintainer via the About section for prompt resolution.")

        else:
            uni_stdcount27 = len(csvdf.values)

            stud_branch = str(df_final['ROLL NO.'].values[0])[3:5]
            stud_cum_cgpa = df_final['CUMULATIVE CGPA'].values[0]
            stud_university_rank = df_final['RANK'].values[0]
            stud_branch_rank = None

            # HAD TO FIND THE BRANCH RANK ALAG SE !
            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR27.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper())
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_total_credits = df_final['CREDITS1'].values[0] + df_final['CREDITS2'].values[0] + \
                                 df_final['CREDITS3'].values[0] + df_final['CREDITS4'].values[0]
            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)
            stud_percentile = round(float(((uni_stdcount27 - stud_university_rank) / uni_stdcount27) * 100), 3)

            stud_grade1List = (df_final['GRADE1'].values[0].replace("[", '').replace("]", '').replace("'", '')).split(
                ',')
            stud_grade2List = (df_final['GRADE2'].values[0].replace("[", '').replace("]", '').replace("'", '')).split(
                ',')
            stud_grade3List = (df_final['GRADE3'].values[0].replace("[", '').replace("]", '').replace("'", '')).split(
                ',')
            stud_grade4List = (df_final['GRADE4'].values[0].replace("[", '').replace("]", '').replace("'", '')).split(
                ',')

            if len(stud_grade1List) < 7:
                for _ in range((7 - len(stud_grade1List))): stud_grade1List.append('  ')
            if len(stud_grade2List) < 7:
                for _ in range((7 - len(stud_grade2List))): stud_grade2List.append('  ')
            if len(stud_grade3List) < 7:
                for _ in range((7 - len(stud_grade3List))): stud_grade3List.append('  ')
            if len(stud_grade4List) < 7:
                for _ in range((7 - len(stud_grade4List))): stud_grade4List.append('  ')

            # MENU1: FIRST MAIN DIV WITH 3 COLUMNS ---------------------------------------------
            l_sec1, m_sec1, r_sec1 = st.columns([1.5, 2, 1])

            with l_sec1:

                st.markdown('<br><br>', unsafe_allow_html=True)

                st.write(f"""
                            <div class="blue-header">HELLO, {df_final["NAME"].values[0]}</div>
                            <h5>{stud_branch}, {shortf_branch27[stud_branch]}, B. TECH</h5>
                            <h5>{df_final['ROLL NO.'].values[0]}</h5>
                            <h5>YOUR RESULTS:</h5>
                            """,
                         unsafe_allow_html=True)

                l1, l2, l3, l4 = st.columns(4)
                l1.metric(label="**SEM 1 | SGPA**", value=+df_final['SGPA1'].values[0])
                l2.metric(label="**SEM 2 | SGPA**", value=+df_final['SGPA2'].values[0],
                          delta=round(float(df_final['SGPA2'].values[0]) - float(df_final['SGPA1'].values[0]), 2))
                l3.metric(label="**SEM 3 | SGPA**", value=+df_final['SGPA3'].values[0],
                          delta=round(float(df_final['SGPA3'].values[0]) - float(df_final['SGPA2'].values[0]), 2))
                l4.metric(label="**SEM 4 | SGPA**", value=+df_final['SGPA4'].values[0],
                          delta=round(float(df_final['SGPA4'].values[0]) - float(df_final['SGPA3'].values[0]), 2))

            with m_sec1:

                st.markdown('<br><br><br>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                            | Credits Completed | Cumulative CGPA | University Rank | Dept Rank |
                            | :------------ | :--------------- | :---------------| :---------------|
                            | {stud_total_credits}<br> | {df_final['CUMULATIVE CGPA'].values[0]}<br> | {stud_university_rank}<br> | {stud_branch_rank}<br> |
                            """,
                    unsafe_allow_html=True,
                )
                st.markdown('<br>', unsafe_allow_html=True)

                # UNIVERSITY PERCENTILE STATS LINE:
                if 0 <= stud_percentile <= 30:
                    uni_tile = random.choice(cat_0_30).replace('__X__', str(stud_percentile)).replace('__TYPE__',
                                                                                                      'university')
                elif 30 < stud_percentile <= 50:
                    uni_tile = random.choice(cat_30_50).replace('__X__', str(stud_percentile)).replace('__TYPE__',
                                                                                                       'university')
                elif 50 < stud_percentile <= 70:
                    uni_tile = random.choice(cat_50_70).replace('__X__', str(round(100 - stud_percentile, 3))).replace(
                        '__TYPE__', 'university')
                elif 70 < stud_percentile <= 100:
                    uni_tile = random.choice(cat_70_100).replace('__X__', str(round(100 - stud_percentile, 3))).replace(
                        '__TYPE__', 'university')

                # UNIVERSITY PERCENTILE STATS LINE:
                if 0 <= stud_brnch_percentile <= 30:
                    dept_tile = random.choice(cat_0_30).replace('__X__', str(stud_brnch_percentile)).replace('__TYPE__',
                                                                                                             'department')
                elif 30 < stud_brnch_percentile <= 50:
                    dept_tile = random.choice(cat_30_50).replace('__X__', str(stud_brnch_percentile)).replace(
                        '__TYPE__',
                        'department')
                elif 50 < stud_brnch_percentile <= 70:
                    dept_tile = random.choice(cat_50_70).replace('__X__',
                                                                 str(round(100 - stud_brnch_percentile, 3))).replace(
                        '__TYPE__',
                        'department')
                elif 70 < stud_brnch_percentile <= 100:
                    dept_tile = random.choice(cat_70_100).replace('__X__',
                                                                  str(round(100 - stud_brnch_percentile, 3))).replace(
                        '__TYPE__',
                        'department')
                st.write('---')
                st.write(f"""{dept_tile}""", unsafe_allow_html=True)
                st.write(f"""{uni_tile}""", unsafe_allow_html=True)
                st.write('---')

            with r_sec1:

                st.markdown('<br><br>', unsafe_allow_html=True)

                st_lottie(
                    load_lottieurl(True, "./animation/flying_student.json"),
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="low",  # medium ; highhh
                    height=None,
                    width=None,
                    key=None,
                )

            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin: 20px;">
                <table style="width: 80%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 14px; color: #ffffff; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); background-color: #121212; border-radius: 12px; overflow: hidden;">
                    <thead>
                        <tr style="background-color: #1F1F1F; text-align: center;">
                            <th style="padding: 12px; border: 1px solid #333;">Semester</th>
                            <th style="padding: 12px; border: 1px solid #333;">S1</th>
                            <th style="padding: 12px; border: 1px solid #333;">S2</th>
                            <th style="padding: 12px; border: 1px solid #333;">S3</th>
                            <th style="padding: 12px; border: 1px solid #333;">S4</th>
                            <th style="padding: 12px; border: 1px solid #333;">S5</th>
                            <th style="padding: 12px; border: 1px solid #333;">S6</th>
                            <th style="padding: 12px; border: 1px solid #333;">S7</th>
                            <th style="padding: 12px; border: 1px solid #333;">Credits</th>
                            <th style="padding: 12px; border: 1px solid #333;">SGPA</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="text-align: center;">
                            <td style="padding: 12px; border: 1px solid #333; background-color: #1a1a1a; color: #3d82f2; font-weight: bold;">SEM 1</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[1]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[2]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[3]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[4]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[5]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade1List[6]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['CREDITS1'].values[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['SGPA1'].values[0]}</td>
                        </tr>
                        <tr style="text-align: center;">
                            <td style="padding: 12px; border: 1px solid #333; background-color: #1a1a1a; color: #3d82f2; font-weight: bold;">SEM 2</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade2List[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade2List[1]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade2List[2]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade2List[3]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade2List[4]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade2List[5]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade2List[6]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['CREDITS2'].values[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['SGPA2'].values[0]}</td>
                        </tr>
                        <tr style="text-align: center;">
                            <td style="padding: 12px; border: 1px solid #333; background-color: #1a1a1a; color: #3d82f2; font-weight: bold;">SEM 3</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade3List[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade3List[1]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade3List[2]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade3List[3]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade3List[4]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade3List[5]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade3List[6]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['CREDITS3'].values[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['SGPA3'].values[0]}</td>
                        </tr>
                        <tr style="text-align: center;">
                            <td style="padding: 12px; border: 1px solid #333; background-color: #1a1a1a; color: #3d82f2; font-weight: bold;">SEM 4</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade4List[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade4List[1]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade4List[2]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade4List[3]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade4List[4]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade4List[5]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{stud_grade4List[6]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['CREDITS4'].values[0]}</td>
                            <td style="padding: 10px; border: 1px solid #333; background-color: #262626;">{df_final['SGPA4'].values[0]}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

                        """, unsafe_allow_html=True)

            st.markdown('---')

            # MENU1: SECOND MAIN DIV WITH 2 COLUMNS ---------------------------------------------

            st.write(f"""
                                    <h3 style="
                                    text-align: center;
                                    align-items: center;
                                    ">Your Branch <span style="color: {color};">{stud_branch}'27</span> and Your CGPA Distribution Stats:</h3>
                                    """, unsafe_allow_html=True)

            _, l_sec2, _, r_sec2, _ = st.columns([0.9, 3.1, 1, 3.1, 0.5])

            with l_sec2:

                df = pd.DataFrame({
                    'Branch Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [max(fl['CUMULATIVE CGPA'].values),
                             round(statistics.mean(fl['CUMULATIVE CGPA'].values), 2),
                             stud_cum_cgpa,
                             round(statistics.mode(fl['CUMULATIVE CGPA'].values), 2),
                             min(fl['CUMULATIVE CGPA'].values)]})

                df.reset_index(drop=True)
                df.set_index('Branch Stats', inplace=True)

                st.plotly_chart(
                    px.bar(df, title=f"{stud_branch}'27 CGPA Distribution", range_y=[0, 10], text_auto='', width=430,
                           color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),
                    config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'zoomOut2d', 'select2d']})

            with r_sec2:

                df = pd.DataFrame({
                    'University Stats': ['Highest', 'Average', 'Your', 'Max Appeared', 'Lowest'],
                    'CGPA': [max(csvdf['CUMULATIVE CGPA'].values),
                             round(statistics.mean(csvdf['CUMULATIVE CGPA'].values), 2),
                             stud_cum_cgpa,
                             round(statistics.mode(csvdf['CUMULATIVE CGPA'].values), 2),
                             min(csvdf['CUMULATIVE CGPA'].values)]})

                df.reset_index(drop=True)
                df.set_index('University Stats', inplace=True)

                st.plotly_chart(
                    px.bar(df, title=f'University CGPA Distribution', range_y=[0, 10], text_auto='', width=430,
                           color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),
                    config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'zoomOut2d', 'select2d']})

            df_plot = pd.DataFrame(
                {
                    'SEMESTER': ['1ST SEM', '2ND SEM', '3RD SEM', '4TH SEM'],
                    'CGPA': [df_final['SGPA1'].values[0], df_final['SGPA2'].values[0], df_final['SGPA3'].values[0],
                             df_final['SGPA4'].values[0]]
                }
            )

            _, mid, _ = st.columns([1, 4, 1])

            with mid:
                st.plotly_chart(
                    px.line(df_plot, x="SEMESTER", y="CGPA", title='YOUR CGPA CHART:').update_layout(
                        {'dragmode': False}), use_container_width=True)

            st.markdown('<br>', unsafe_allow_html=True)
            # MENU1: THIRD MAIN DIV WITH 1 COLUMNS--------------------------------------------------------------------------------------------------

            st.markdown('---')

            df = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR27.csv', dtype=str,
                             index_col=None).fillna("")
            df = df[['RANK', 'NAME', 'ROLL NO.', 'SGPA1', 'SGPA2', 'SGPA3', 'SGPA4', 'CUMULATIVE CGPA']]
            df.columns = ['RANK', 'NAME', 'ROLL NO.', '1ST SEM', '2ND SEM', '3RD SEM', '4TH SEM', 'CUMULATIVE CGPA']

            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{stud_branch}'27</span> Students Rankings: </h3>
                        """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            _, mm, _ = st.columns([1, 4, 1])
            with mm:
                ranklist = st.empty()
                ranklist.dataframe(df, hide_index=True, use_container_width=True, height=425)

                st.markdown("<br>", unsafe_allow_html=True)

            _, _, mm2, _, _ = st.columns([2, 1, 1, 1, 2])
            with mm2:
                gainerButton = st.button("WANNA SEE THE TOP GAINERS THIS SEM?")
                if gainerButton:
                    gainerList(stud_branch)

            st.markdown('---')

            # MENU1: FOURTH MAIN DIV WITH 3 COLUMNS --------------------------------------------------------------------------------------------------

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

            avg_placement_barc = px.bar(df, title=f"Average Package Trend (IN LPA)", text_auto='',
                                        color_discrete_sequence=[BAR_COLOR]).update_layout(
                {'dragmode': False})

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

            max_placement_barc = px.bar(df, title=f"Highest Package Trend (IN LPA)", text_auto='',
                                        color_discrete_sequence=[BAR_COLOR]).update_layout(
                {'dragmode': False})

            # PERCENTAGE PLACED PLACEMENT

            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                '% STUDENT PLACED': [
                    float(
                        data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace(
                            '%',
                            '')),
                    float(
                        data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace(
                            '%',
                            '')),
                    float(
                        data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace(
                            '%',
                            ''))
                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            percent_placement_barc = px.bar(df, title=f"Percentage Of Student Placed", range_y=[0, 100],
                                            text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
                {'dragmode': False})

            bar1, bar2, bar3 = st.columns(3)
            with bar1:
                st.plotly_chart(avg_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})
            with bar2:
                st.plotly_chart(max_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})
            with bar3:
                st.plotly_chart(percent_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})

            add_report_card_button(df_final, stud_branch, shortf_branch27, stud_university_rank,
                                   stud_branch_rank, stud_percentile, stud_brnch_percentile, stud_total_credits)

    elif year_choosed == '2026 (NOT UPDATED YET)' and result_search_box:

        descripE.empty()
        st.session_state.yeartitle = '2026'

        # IF USER HAS PUTTEN 2K/2k IN THE ROLL NUMBER, REMOVING THAT CAUSE, OUR DATA DOES NOT CONTAIN THAT
        if '2k' in result_search_box or '2K' in result_search_box:
            result_search_box = result_search_box.replace('2k', '').replace('2K', '').strip()

        # DEALING WITH USER PUTTEN ROLL NO. 23/EP/12  AND  23/EP/01
        if len(result_search_box) == 8:
            result_search_box = result_search_box[0:6] + '0' + result_search_box[6:]

        data26std = pd.read_csv('Extracting_Result_Data/ranked_results_csv/UNI_rankedR26.csv')
        m1 = data26std['ROLL NO.'].str.contains(result_search_box.upper())
        df_final = data26std[m1]

        uni_stdcount26 = len(data26std.values)

        if (len(df_final) > 1 or len(df_final) < 1) and not other:
            st.markdown('<br><br><br>', unsafe_allow_html=True)
            _, mmn, _ = st.columns([0.5,2.5,0.5])
            mmn.error(
                "If your result is not found or appears incorrect—despite being extracted from official result PDFs—please verify your roll number and, if the issue persists, contact the project maintainer via the About section for prompt resolution.")

        elif len(df_final) == 1:

            stud_branch = str(df_final['ROLL NO.'].values[0])[3:5]
            stud_cum_cgpa = df_final['CUMULATIVE CGPA'].values[0]
            stud_branch_rank = None
            stud_university_rank = df_final['RANK'].values[0]

            # HAD TO FIND THE BRANCH RANK ALAG SE !
            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR26.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper())
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 4)
            stud_percentile = round(float(((uni_stdcount26 - stud_university_rank) / uni_stdcount26) * 100), 4)

            l_c, m_c, r_c = st.columns([1.5, 2, 1])

            with l_c:

                st.markdown('<br><br>', unsafe_allow_html=True)

                st.write(f"""
                            <h2 style="color: #1F51FF;">HELLO, {df_final['NAME'].values[0]}</h2>
                            <h5>{stud_branch}, {shortf_branch26[stud_branch]}, B. TECH</h5>
                            <h5>{df_final['ROLL NO.'].values[0]}</h5>
                            <h5>RESULTS:- </h5>
                            """,
                         unsafe_allow_html=True)

                l1, l2, l3, l4 = st.columns(4)
                l1.metric(label="**1ST SEM CG**", value=df_final['SGPA1'].values[0])
                l2.metric(label="**2ND SEM CG**", value=df_final['SGPA2'].values[0],
                          delta=round(float(df_final['SGPA2'].values[0]) - float(df_final['SGPA1'].values[0]), 2))
                l3.metric(label="**3RD SEM CG**", value=df_final['SGPA3'].values[0],
                          delta=round(float(df_final['SGPA3'].values[0]) - float(df_final['SGPA2'].values[0]), 2))
                l4.metric(label="**4TH SEM CG**", value=df_final['SGPA4'].values[0],
                          delta=round(float(df_final['SGPA4'].values[0]) - float(df_final['SGPA3'].values[0]), 2))

            with m_c:

                st.markdown('<br><br><br>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                            | Cumulative CGPA | University Rank | Dept Rank |
                            | :--------------- | :---------------| :---------------|
                            | {df_final['CUMULATIVE CGPA'].values[0]}<br> | {stud_university_rank}<br> | {stud_branch_rank}<br> |
                            """,
                    unsafe_allow_html=True,
                )
                st.markdown('<br><br>', unsafe_allow_html=True)

                if stud_percentile > 50:
                    st.write(f"""
                            <h5> | You are in TOP <span style="color: #87CEFA;">{round(100 - stud_percentile, 3)}%</span> Students of University |</h5>
                            """, unsafe_allow_html=True)
                else:
                    st.write(f"""
                            <h5> | You Performed better than <span style="color: #87CEFA;">{round(stud_percentile, 3)}%</span> Students of University | </h5>
                            """, unsafe_allow_html=True)

                st.markdown('<br>', unsafe_allow_html=True)

                if stud_brnch_percentile > 50:
                    st.write(f"""
                            <h5> | You are in TOP <span style="color: #87CEFA;">{round(100 - stud_brnch_percentile, 3)}%</span> Students of your Dept | </h5>
                            """, unsafe_allow_html=True)
                else:
                    st.write(f"""
                            <h5> | You Performed better than <span style="color: #87CEFA;">{round(stud_brnch_percentile, 3)}%</span> Students of your Dept | </h5>
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

                brnch_cg = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR26.csv',
                                       index_col=False)

                df = pd.DataFrame({
                    'Branch Stats': ['Highest', 'Average', 'Your', 'Max Appeared'],
                    'CGPA': [max(brnch_cg['CUMULATIVE CGPA'].values),
                             round(statistics.mean(brnch_cg['CUMULATIVE CGPA'].values), 4),
                             stud_cum_cgpa, round(statistics.mode(brnch_cg['CUMULATIVE CGPA'].values), 4)]})

                df.reset_index(drop=True)
                df.set_index('Branch Stats', inplace=True)

                st.plotly_chart(px.bar(df, title=f"{stud_branch}'26 CGPA Distribution 2026", text_auto='',
                                       color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),
                                use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d', 'zoomOut2d']})

            with right_c:

                uni_cg = pd.read_csv('Extracting_Result_Data/ranked_results_csv/UNI_rankedR26.csv', index_col=False)

                df = pd.DataFrame({
                    'University Stats': ['Highest', 'Average', 'Your', 'Max Appeared'],
                    'CGPA': [max(uni_cg['CUMULATIVE CGPA'].values),
                             round(statistics.mean(uni_cg['CUMULATIVE CGPA'].values), 4),
                             stud_cum_cgpa, round(statistics.mode(uni_cg['CUMULATIVE CGPA'].values), 4)]})

                df.reset_index(drop=True)
                df.set_index('University Stats', inplace=True)

                st.plotly_chart(px.bar(df, title=f'University CGPA Distribution 2026', text_auto='',
                                       color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False}),
                                use_container_width=True, config={
                        "modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d', 'zoomOut2d',
                                                   'hoverClosestCartesian']})

            df1 = pd.DataFrame(
                {
                    'SEMESTER': ['1ST SEM', '2ND SEM', '3RD SEM', '4TH SEM'],
                    'CGPA': [df_final['SGPA1'].values[0], df_final['SGPA2'].values[0], df_final['SGPA3'].values[0],
                             df_final['SGPA4'].values[0]]
                }
            )

            _, mid, _ = st.columns([1, 2.5, 1])
            with mid:
                st.plotly_chart(
                    px.line(df1, x="SEMESTER", y="CGPA", title='YOUR CGPA CHART: ', range_y=[0, 10]).update_layout(
                        {'dragmode': False}), use_container_width=True)

            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown("---")

            df = pd.read_csv(
                f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR26.csv',
                dtype=str,
                index_col=None).fillna("")

            df = df[['RANK', 'NAME', 'ROLL NO.', 'SGPA1', 'SGPA2', 'SGPA3', 'SGPA4', 'CUMULATIVE CGPA']]
            df.columns = ['RANK', 'NAME', 'ROLL NO.', 'SEM 1', 'SEM 2', 'SEM 3', 'SEM 4', 'CUMULATIVE CGPA']

            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{stud_branch}'26 </span> Students Rankings: </h3>
                        """,
                     unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            _, mm, _ = st.columns([0.7, 4, 0.7])
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

            avg_placement_barc = px.bar(df, title=f"Average Package Trend (IN LPA)", text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
                {'dragmode': False})

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

            max_placement_barc = px.bar(df, title=f"Highest Package Trend (IN LPA)", text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout(
                {'dragmode': False})

            # PERCENTAGE PLACED PLACEMENT

            data23 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed23.csv')
            data22 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed22.csv')
            data21 = pd.read_csv('./Extracting_Result_Data/placement_data/percentage_placed21.csv')

            df = pd.DataFrame({
                'YEAR': ['2023', '2022', '2021'],
                '% STUDENT PLACED': [
                    float(
                        data23.loc[data23['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace(
                            '%', '')),
                    float(
                        data22.loc[data22['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace(
                            '%', '')),
                    float(
                        data21.loc[data21['Branch'] == placem_branch_name[stud_branch]]['Placed (%)'].values[0].replace(
                            '%', ''))
                ]})

            df.reset_index(drop=True)
            df.set_index('YEAR', inplace=True)

            percent_placement_barc = px.bar(df, title=f"Percentage Of Student Placed", range_y=[0, 100],
                                            text_auto='', color_discrete_sequence=[BAR_COLOR]).update_layout({'dragmode': False})

            bar1, bar2, bar3 = st.columns(3)
            with bar1:
                st.plotly_chart(avg_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})
            with bar2:
                st.plotly_chart(max_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})
            with bar3:
                st.plotly_chart(percent_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})

            st.markdown("---")

# ELIF CASES FOR CALLING OUT THE OTHER MENU FUNCTIONS!

elif selected == 'RANKS':
    ranksNresults_menu()

elif selected == 'PLACEMENTS':
    placement_menu()

elif selected == 'ABOUT':
    aboutsection_menu()

elif selected == 'STUDY':
    studyResources_menu()


# END OF THE CODE
