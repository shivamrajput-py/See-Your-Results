import io
import re

with io.open('1_STUDENT_PROFILE.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace padding
code = re.sub(
    r"        if len\(result_search_box\) == 9:\n            result_search_box = result_search_box\[0:7\] \+ '0' \+ result_search_box\[7:\]",
    '''        parts = result_search_box.split('/')\n        if len(parts) == 3 and len(parts[-1]) < 3:\n            parts[-1] = parts[-1].zfill(3)\n            result_search_box = '/'.join(parts)''',
    code
)

code = re.sub(
    r"        if len\(result_search_box\) == 8:\n            result_search_box = result_search_box\[0:6\] \+ '0' \+ result_search_box\[6:\]",
    '''        parts = result_search_box.split('/')\n        if len(parts) == 3 and len(parts[-1]) < 3:\n            parts[-1] = parts[-1].zfill(3)\n            result_search_box = '/'.join(parts)''',
    code
)

# 2028 Rank fallback
code = code.replace(
'''            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR28.csv')
            m1 = fl['ROLL NO. OG'].str.contains(result_search_box.upper(), regex=False, na=False)
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_total_credits = df_final['CREDITS1'].values[0]

            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)''',
'''            try:
                fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR28.csv')
                m1_fl = fl['ROLL NO. OG'].str.contains(result_search_box.upper(), regex=False, na=False)
                fl_final = fl[m1_fl]
                stud_branch_rank = int(fl_final['RANK'].values[0]) if len(fl_final) > 0 else "N/A"
            except Exception:
                fl = csvdf
                stud_branch_rank = "N/A"

            stud_total_credits = df_final['CREDITS1'].values[0]

            if stud_branch_rank != "N/A":
                stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)
            else:
                stud_brnch_percentile = 0.0'''
)

# 2027 Rank fallback
code = code.replace(
'''            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR27.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_total_credits = df_final['CREDITS1'].values[0] + df_final['CREDITS2'].values[0] + \\
                                 df_final['CREDITS3'].values[0] + df_final['CREDITS4'].values[0]
            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)''',
'''            try:
                fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR27.csv')
                m1_fl = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
                fl_final = fl[m1_fl]
                stud_branch_rank = int(fl_final['RANK'].values[0]) if len(fl_final) > 0 else "N/A"
            except Exception:
                fl = csvdf
                stud_branch_rank = "N/A"

            stud_total_credits = df_final['CREDITS1'].values[0] + df_final['CREDITS2'].values[0] + \\
                                 df_final['CREDITS3'].values[0] + df_final['CREDITS4'].values[0]

            if stud_branch_rank != "N/A":
                stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 3)
            else:
                stud_brnch_percentile = 0.0'''
)

# 2026 Rank fallback
code = code.replace(
'''            fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR26.csv')
            m1 = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
            fl_final = fl[m1]
            stud_branch_rank = fl_final['RANK'].values[0]
            stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 4)''',
'''            try:
                fl = pd.read_csv(f'./Extracting_Result_Data/ranked_results_csv/{stud_branch}_rankedR26.csv')
                m1_fl = fl['ROLL NO.'].str.contains(result_search_box.upper(), regex=False, na=False)
                fl_final = fl[m1_fl]
                stud_branch_rank = int(fl_final['RANK'].values[0]) if len(fl_final) > 0 else "N/A"
            except Exception:
                fl = data26std
                stud_branch_rank = "N/A"

            if stud_branch_rank != "N/A":
                stud_brnch_percentile = round(float(((len(fl.values) - stud_branch_rank) / len(fl.values)) * 100), 4)
            else:
                stud_brnch_percentile = 0.0'''
)

safe_fetch = '''
def __safe_pkg_val(df, branch, placem_branch_name, col_name, as_float=False):
    import pandas as pd
    try:
        val = df.loc[df['Branch'] == placem_branch_name.get(branch, '')][col_name].values[0]
        if as_float:
            return float(str(val).replace('%', ''))
        return float(val) if not as_float else val
    except Exception:
        return 0.0

st.set_page_config'''
code = code.replace('st.set_page_config', safe_fetch, 1)

code = re.sub(
    r"data23\.loc\[data23\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Avg CTC \(in LPA\)'\]\.values\[0\]",
    "__safe_pkg_val(data23, stud_branch, placem_branch_name, 'Avg CTC (in LPA)')",
    code
)
code = re.sub(
    r"data22\.loc\[data22\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Avg CTC \(in LPA\)'\]\.values\[0\]",
    "__safe_pkg_val(data22, stud_branch, placem_branch_name, 'Avg CTC (in LPA)')",
    code
)
code = re.sub(
    r"data21\.loc\[data21\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Avg CTC \(in LPA\)'\]\.values\[0\]",
    "__safe_pkg_val(data21, stud_branch, placem_branch_name, 'Avg CTC (in LPA)')",
    code
)

code = re.sub(
    r"data23\.loc\[data23\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Max CTC \(in LPA\)'\]\.values\[0\]",
    "__safe_pkg_val(data23, stud_branch, placem_branch_name, 'Max CTC (in LPA)')",
    code
)
code = re.sub(
    r"data22\.loc\[data22\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Max CTC \(in LPA\)'\]\.values\[0\]",
    "__safe_pkg_val(data22, stud_branch, placem_branch_name, 'Max CTC (in LPA)')",
    code
)
code = re.sub(
    r"data21\.loc\[data21\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Max CTC \(in LPA\)'\]\.values\[0\]",
    "__safe_pkg_val(data21, stud_branch, placem_branch_name, 'Max CTC (in LPA)')",
    code
)

code = re.sub(
    r"float\(\s*data23\.loc\[data23\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Placed \(%\)'\]\.values\[0\]\.replace\(\s*'%',\s*''\)\)",
    "__safe_pkg_val(data23, stud_branch, placem_branch_name, 'Placed (%)', as_float=True)",
    code
)
code = re.sub(
    r"float\(\s*data22\.loc\[data22\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Placed \(%\)'\]\.values\[0\]\.replace\(\s*'%',\s*''\)\)",
    "__safe_pkg_val(data22, stud_branch, placem_branch_name, 'Placed (%)', as_float=True)",
    code
)
code = re.sub(
    r"float\(\s*data21\.loc\[data21\['Branch'\] == placem_branch_name\[stud_branch\]\]\['Placed \(%\)'\]\.values\[0\]\.replace\(\s*'%',\s*''\)\)",
    "__safe_pkg_val(data21, stud_branch, placem_branch_name, 'Placed (%)', as_float=True)",
    code
)

code = re.sub(r'shortf_branch28\[stud_branch\]', 'shortf_branch28.get(stud_branch, stud_branch)', code)
code = re.sub(r'shortf_branch27\[stud_branch\]', 'shortf_branch27.get(stud_branch, stud_branch)', code)
code = re.sub(r'shortf_branch26\[stud_branch\]', 'shortf_branch26.get(stud_branch, stud_branch)', code)

with io.open('1_STUDENT_PROFILE.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('SUCCESS!')
