import io

with io.open('1_STUDENT_PROFILE.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix roll number logic 2028
old1 = '''        # DEALING WITH USER PUTTEN ROLL NO. 24/B12/04  AND  24/B12/04
        if len(result_search_box) == 9:
            result_search_box = result_search_box[0:7] + '0' + result_search_box[7:]'''
new1 = '''        # DEALING WITH USER PUTTEN ROLL NO.
        parts = result_search_box.split('/')
        if len(parts) == 3 and len(parts[-1]) < 3:
            parts[-1] = parts[-1].zfill(3)
            result_search_box = '/'.join(parts)'''
code = code.replace(old1, new1)

# Fix roll number logic 2027 and 2026
old2 = '''        # DEALING WITH USER PUTTEN ROLL NO. 23/EP/12  AND  23/EP/01
        if len(result_search_box) == 8:
            result_search_box = result_search_box[0:6] + '0' + result_search_box[6:]'''
new2 = '''        # DEALING WITH USER PUTTEN ROLL NO.
        parts = result_search_box.split('/')
        if len(parts) == 3 and len(parts[-1]) < 3:
            parts[-1] = parts[-1].zfill(3)
            result_search_box = '/'.join(parts)'''
code = code.replace(old2, new2)

old3 = '''            # HAD TO FIND THE BRANCH RANK ALAG SE !
            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR28.csv')
            m1 = fl['ROLL NO. OG'].str.contains(result_search_box.upper(), regex=False, na=False)
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_total_credits = df_final['CREDITS1'].values[0]

            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)'''
new3 = '''            # HAD TO FIND THE BRANCH RANK ALAG SE !
            try:
                fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR28.csv')
                m1_fl = fl['ROLL NO. OG'].str.contains(result_search_box.upper(), regex=False, na=False)
                fl_final = fl[m1_fl]
                if len(fl_final) > 0:
                    stud_branch_rank = int(fl_final['RANK'].values[0])
                else:
                    stud_branch_rank = "N/A"
            except Exception:
                fl = csvdf
                stud_branch_rank = "N/A"

            stud_total_credits = df_final['CREDITS1'].values[0]

            if stud_branch_rank != "N/A":
                stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)
            else:
                stud_brnch_percentile = 0.0'''
code = code.replace(old3, new3)

# Fix 2027 logic
old4 = '''            # HAD TO FIND THE BRANCH RANK ALAG SE !
            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR27.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_total_credits = df_final['CREDITS1'].values[0] + df_final['CREDITS2'].values[0] + \\
                                 df_final['CREDITS3'].values[0] + df_final['CREDITS4'].values[0]
            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)'''
new4 = '''            # HAD TO FIND THE BRANCH RANK ALAG SE !
            try:
                fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR27.csv')
                m1_fl = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
                fl_final = fl[m1_fl]
                if len(fl_final) > 0:
                    stud_branch_rank = int(fl_final['RANK'].values[0])
                else:
                    stud_branch_rank = "N/A"
            except Exception:
                fl = csvdf
                stud_branch_rank = "N/A"

            stud_total_credits = df_final['CREDITS1'].values[0] + df_final['CREDITS2'].values[0] + \\
                                 df_final['CREDITS3'].values[0] + df_final['CREDITS4'].values[0]

            if stud_branch_rank != "N/A":
                stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)
            else:
                stud_brnch_percentile = 0.0'''
code = code.replace(old4, new4)

# Fix 2026 logic
old5 = '''            # HAD TO FIND THE BRANCH RANK ALAG SE !
            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR26.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 4)'''
new5 = '''            # HAD TO FIND THE BRANCH RANK ALAG SE !
            try:
                fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR26.csv')
                m1_fl = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
                fl_final = fl[m1_fl]
                if len(fl_final) > 0:
                    stud_branch_rank = int(fl_final['RANK'].values[0])
                else:
                    stud_branch_rank = "N/A"
            except Exception:
                fl = data26std
                stud_branch_rank = "N/A"

            if stud_branch_rank != "N/A":
                stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 4)
            else:
                stud_brnch_percentile = 0.0'''
code = code.replace(old5, new5)

# Fix Placements 2028
old6 = '''            st.write(f"""<h3 style="text-align: center; align-items: center;">Your Branch <span style="color: {color};">{shortf_branch28[stud_branch]}</span> Placement Stats:</h3>""",unsafe_allow_html=True)'''
new6 = '''            try:
                st.write(f"""<h3 style="text-align: center; align-items: center;">Your Branch <span style="color: {color};">{shortf_branch28[stud_branch]}</span> Placement Stats:</h3>""",unsafe_allow_html=True)'''
code = code.replace(old6, new6)

old7 = '''            with bar3:
                st.plotly_chart(percent_placement_barc, use_container_width=True,config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})'''
new7 = '''            with bar3:
                st.plotly_chart(percent_placement_barc, use_container_width=True,config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})
            except Exception:
                st.info('Placement stats are currently unavailable for this branch.')'''
code = code.replace(old7, new7)

# Fix Placements 2027
old8 = '''            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{shortf_branch27[stud_branch]}</span> Placement Stats:</h3>
                        """,
                     unsafe_allow_html=True)'''
new8 = '''            try:
                st.write(f"""
                            <h3 style="
                            text-align: center;
                            align-items: center;
                            ">Your Branch <span style="color: {color};">{shortf_branch27[stud_branch]}</span> Placement Stats:</h3>
                            """,
                         unsafe_allow_html=True)'''
code = code.replace(old8, new8)

old9 = '''            with bar3:
                st.plotly_chart(percent_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})'''
new9 = '''            with bar3:
                st.plotly_chart(percent_placement_barc, use_container_width=True,
                                config={"modeBarButtonsToRemove": ['lasso2d', 'autoScale2d', 'select2d']})
            except Exception:
                st.info('Placement stats are currently unavailable for this branch.')'''
code = code.replace(old9, new9)

# Fix Placements 2026
old10 = '''            st.write(f"""
                        <h3 style="
                        text-align: center;
                        align-items: center;
                        ">Your Branch <span style="color: {color};">{shortf_branch26[stud_branch]}</span> Placement Stats:</h3>
                        """,
                     unsafe_allow_html=True)'''
new10 = '''            try:
                st.write(f"""
                            <h3 style="
                            text-align: center;
                            align-items: center;
                            ">Your Branch <span style="color: {color};">{shortf_branch26[stud_branch]}</span> Placement Stats:</h3>
                            """,
                         unsafe_allow_html=True)'''
code = code.replace(old10, new10)

with io.open('1_STUDENT_PROFILE.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('SUCCESS!', 'Count parts = result_search_box.split:', code.count('parts = result_search_box.split'), 'try-except chunks missing:', code.count('except Exception:'))
