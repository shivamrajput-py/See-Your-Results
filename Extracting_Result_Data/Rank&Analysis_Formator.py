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

    INFO = {}

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

        # CG ANALYSIS OF THESE BRANCH CG
        cg_list_branchwise = branch_wise['CUMULATIVE CGPA'].values[:]

        if len(cg_list_branchwise)<1: continue

        INFO[branch] = {
                    'Average': statistics.mean(cg_list_branchwise),
                    'Median': statistics.median(cg_list_branchwise),
                    'Mode': statistics.mode(cg_list_branchwise),
                    'Highest': max(cg_list_branchwise),
                    'Lowest': min(cg_list_branchwise)
        }

    #---------------------------------------------------------------------------------------------------------------------------

    # MAIN FINAL UNI SORTED CSV WITH RNK COLUMN
    cum_data = mncsv

    for i, _ in enumerate(cum_data['RANK']):
        cum_data.iloc[i, 0] = i+1

    cum_data.to_csv('./ranked_results_csv/UNI_rankedR27.csv')


    #---------------------------------------------------------------------------------------------------------------------------

    # CG ANALYSIS FOR UNIVERSITY DATA

    cg_list = cum_data['CUMULATIVE CGPA'].values[:]
    INFO['UNI'] = {
            'Average': statistics.mean(cg_list),
            'Median': statistics.median(cg_list),
            'Mode': statistics.mode(cg_list),
            'Highest': max(cg_list),
            'Lowest': min(cg_list)
        }

    # INFO JSON
    # with open('./ranked_results_csv/cg_analysis.json', 'w') as fl:
    #     fl.write(json.dumps(INFO, indent=3))


    #__________________________________CG ANALYSIS CSV BRANCHWISE AND UNIWISE BOTH_________________________________________

    data_file = open('./ranked_results_csv/cg_analysis.csv', 'w')
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(['BRANCH',  'Highest', 'Average' ,'Your', 'Median', 'Max Appeared', 'Lowest'])

    for branch in INFO.keys():

        # Writing data of CSV file
        csv_writer.writerow([branch,
                            INFO[branch]['Highest'],
                            round(INFO[branch]['Average'], 2),
                            None,
                            INFO[branch]['Median'],
                            INFO[branch]['Mode'],
                            INFO[branch]['Lowest']])

    data_file.close()


#2026---------------------------------------------------------------------------------------------------------------------------

if True:

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

        # CG ANALYSIS OF THESE BRANCH CG
        cg_list_branchwise = branch_wise['CUMULATIVE CGPA'].values[:]

        if len(cg_list_branchwise)<1: continue

        INFO[branch] = {
                    'Average': statistics.mean(cg_list_branchwise),
                    'Median': statistics.median(cg_list_branchwise),
                    'Mode': statistics.mode(cg_list_branchwise),
                    'Highest': max(cg_list_branchwise),
                    'Lowest': min(cg_list_branchwise)
        }

    #---------------------------------------------------------------------------------------------------------------------------

    # MAIN FINAL UNI SORTED CSV WITH RNK COLUMN
    cum_data = mncsv

    for i, _ in enumerate(cum_data['RANK']):
        cum_data.iloc[i, 0] = i+1

    cum_data.to_csv('./ranked_results_csv/UNI_rankedR26.csv')


    #---------------------------------------------------------------------------------------------------------------------------

    # CG ANALYSIS FOR UNIVERSITY DATA

    # cg_list = cum_data['CUMULATIVE CGPA'].values[:]
    # INFO['UNI'] = {
    #         'Average': statistics.mean(cg_list),
    #         'Median': statistics.median(cg_list),
    #         'Mode': statistics.mode(cg_list),
    #         'Highest': max(cg_list),
    #         'Lowest': min(cg_list)
    #     }

    # INFO JSON
    # with open('./ranked_results_csv/cg_analysis_26.json', 'w') as fl:
    #     fl.write(json.dumps(INFO, indent=3))


    #__________________________________CG ANALYSIS CSV BRANCHWISE AND UNIWISE BOTH_________________________________________

    # data_file = open('./ranked_results_csv/cg_analysis_26.csv', 'w')
    # csv_writer = csv.writer(data_file)
    # csv_writer.writerow(['BRANCH',  'Highest', 'Average' ,'Your', 'Median', 'Max Appeared', 'Lowest'])
    #
    # for branch in INFO.keys():
    #
    #     # Writing data of CSV file
    #     csv_writer.writerow([branch,
    #                         INFO[branch]['Highest'],
    #                         round(INFO[branch]['Average'], 2),
    #                         None,
    #                         INFO[branch]['Median'],
    #                         INFO[branch]['Mode'],
    #                         INFO[branch]['Lowest']])
    #
    # data_file.close()