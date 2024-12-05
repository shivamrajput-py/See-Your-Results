import json
import statistics
import csv
import pandas as pd

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

#2027---------------------------------------------------------------------------------------------------------------------------

if False:


    # BRANCH WISE SEPARATION OF SORTED CSV WITH RANK COLUMNS
    mncsv = pd.read_csv("./ranked_results_csv/27Batch_allStudent.csv")

    for branch in shortf_branch27.keys():

        m1 = mncsv['ROLL NO.'].str.contains(f'23/{branch}')
        if not (len(m1) > 0): continue
        branch_wise  = mncsv[m1]
        branch_wise = branch_wise.sort_values(by=[branch_wise.columns[-2], branch_wise.columns[1]], ascending=[False, True])
        count = 1
        for row in branch_wise['RANK']:
            branch_wise.iloc[count-1, 0] = count
            count +=1

        # SORTED BRANCHWISE RANKED CSV
        branch_wise.to_csv(f'./ranked_results_csv/{branch}_rankedR27.csv')

    #---------------------------------------------------------------------------------------------------------------------------

    # MAIN FINAL UNI SORTED CSV WITH RNK COLUMN
    cum_data = mncsv

    for i, _ in enumerate(cum_data['RANK']):
        cum_data.iloc[i, 0] = i+1

    cum_data.to_csv('./ranked_results_csv/UNI_rankedR27.csv')


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
if True:
    for branch in shortf_branch27.keys():

        brnch_csv = pd.read_csv(f'./ranked_results_csv/{branch}_rankedR27.csv')

        fll = open(f'./ranked_results_csv/{branch}_gainersR27.csv', 'w')
        gainer_csv = csv.writer(fll)
        gainer_csv.writerow(['RANK','NAME', 'ROLL NO.', 'SEM1', 'SEM2', 'IMPROVEMENT'])

        for i, _ in enumerate(brnch_csv['ROLL NO.'].values):
            gainer_csv.writerow([1, brnch_csv['NAME'].values[i],
                                 brnch_csv['ROLL NO.'].values[i],
                                 brnch_csv['SGPA1'].values[i],
                                 brnch_csv['SGPA2'].values[i],
                                 round(brnch_csv['SGPA2'].values[i]-brnch_csv['SGPA1'].values[i], 3)])

        fll.close()
        gainer_csv= pd.read_csv(f'./ranked_results_csv/{branch}_gainersR27.csv')
        gainer_csv = gainer_csv.sort_values(by= [gainer_csv.columns[-1], gainer_csv.columns[1]], ascending=[False, True])

        for i, _ in enumerate(gainer_csv['RANK'].values):
            gainer_csv.iloc[i, 0] = i + 1

        gainer_csv.to_csv(f'./ranked_results_csv/{branch}_gainersR27.csv')



