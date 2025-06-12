import json
import statistics
import csv
import pandas as pd
from MainConstant import *

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

branch_codes = {
    'CS': ['A01', 'A02', 'A03', 'A04', 'A05', 'A07'],
    'IT': ['A08', 'A09', 'A10'],
    'EC': ['A11', 'A12', 'A13', 'A14'],
    'EE': ['A15', 'A16', 'A17', 'A18', 'A19'],
    'SE': ['B01', 'B02', 'B03'],
    'MC': ['B04', 'B05', 'B06'],
    'EP': ['B07', 'B08'],
    'ME': ['B09', 'B10', 'B11', 'B12'],
    'MAM': ['B13'],
    'PE': ['B14'],
    'CH': ['B15'],
    'CE': ['B16', 'B17'],
    'EN': ['B18'],
    'BT': ['B19']
}

# 2028 BATCH RANKING CODE ---------------------------------------------------------------------------------------------------------------------------

if True:

    # BRANCH WISE SEPARATION OF SORTED CSV WITH RANK COLUMNS
    mncsv = pd.read_csv("./ranked_results_csv/28ALLSTUDENT_TILLS1.csv")

    for branch in branch_codes.keys():
        branch_wise = pd.DataFrame()  # Initialize empty DataFrame for each branch

        for branch_code in branch_codes[branch]:
            m1 = mncsv['ROLL NO.'].str.contains(f'24/{branch_code}')
            if m1.any():  # Check if any matches found
                branch_wise = pd.concat([branch_wise, mncsv[m1]], ignore_index=True)

        if not branch_wise.empty:  # Only process if branch has students
            # Sort by CUMULATIVE CGPA (descending) and then by NAME (ascending)
            branch_wise = branch_wise.sort_values(by=['SGPA1', 'NAME'], ascending=[False, True])

            # Reset index and assign ranks
            branch_wise = branch_wise.reset_index(drop=True)
            branch_wise['RANK'] = range(1, len(branch_wise) + 1)

            # Save branch-wise ranked CSV
            branch_wise.to_csv(f'./ranked_results_csv/{branch}_rankedR28.csv', index=False)

    # ---------------------------------------------------------------------------------------------------------------------------

    # MAIN FINAL UNI SORTED CSV WITH RANK COLUMN
    cum_data = mncsv.copy()

    # Sort by CUMULATIVE CGPA (descending) and then by NAME (ascending)
    cum_data = cum_data.sort_values(by=['SGPA1', 'NAME'], ascending=[False, True])

    # Reset index and assign university ranks
    cum_data = cum_data.reset_index(drop=True)
    cum_data['RANK'] = range(1, len(cum_data) + 1)

    # Save university-wide ranked CSV
    cum_data.to_csv('./ranked_results_csv/UNI_rankedR28.csv', index=False)


#2026---------------------------------------------------------------------------------------------------------------------------

if False:

    INFO = {}

    # BRANCH WISE SEPARATION OF SORTED CSV WITH RANK COLUMNS
    mncsv = pd.read_csv("./ranked_results_csv/UNI_rankedR26.csv")

    for branch in shortf_branch26.keys():

        m1 = mncsv['ROLL NO.'].str.contains(f'22/{branch}')
        if not (len(m1) > 0): continue
        branch_wise  = mncsv[m1]
        branch_wise = branch_wise.sort_values(by=[branch_wise.columns[-1], branch_wise.columns[1]], ascending=[False, True])
        count = 1
        for row in branch_wise['RANK']:
            branch_wise.iloc[count-1, 0] = count
            count +=1

        # SORTED BRANCHWISE RANKED CSV
        branch_wise.to_csv(f'./ranked_results_csv/{branch}_rankedR26.csv')

    #---------------------------------------------------------------------------------------------------------------------------

    # MAIN FINAL UNI SORTED CSV WITH RNK COLUMN
    cum_data = mncsv

    for i, _ in enumerate(cum_data['RANK']):
        cum_data.iloc[i, 0] = i+1

    cum_data.to_csv('./ranked_results_csv/UNI_rankedR26.csv')


#   GAINER CSV MAKERRR ------------------------------------------------------------------
if False:
    for branch in shortf_branch27.keys():

        brnch_csv = pd.read_csv(f'./ranked_results_csv/{branch}_rankedR27.csv')

        fll = open(f'./ranked_results_csv/{branch}_gainersR27.csv', 'w')
        gainer_csv = csv.writer(fll)
        gainer_csv.writerow(['RANK','NAME', 'ROLL NO.', 'SEM2', 'SEM3', 'IMPROVEMENT'])

        for i, _ in enumerate(brnch_csv['ROLL NO.'].values):
            gainer_csv.writerow([1, brnch_csv['NAME'].values[i],
                                 brnch_csv['ROLL NO.'].values[i],
                                 brnch_csv['SGPA2'].values[i],
                                 brnch_csv['SGPA3'].values[i],
                                 round(brnch_csv['SGPA3'].values[i]-brnch_csv['SGPA2'].values[i], 3)])

        fll.close()
        gainer_csv= pd.read_csv(f'./ranked_results_csv/{branch}_gainersR27.csv')
        gainer_csv = gainer_csv.sort_values(by= [gainer_csv.columns[-1], gainer_csv.columns[1]], ascending=[False, True])

        for i, _ in enumerate(gainer_csv['RANK'].values):
            gainer_csv.iloc[i, 0] = i + 1

        gainer_csv.to_csv(f'./ranked_results_csv/{branch}_gainersR27.csv')



