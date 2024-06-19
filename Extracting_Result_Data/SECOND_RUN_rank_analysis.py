import json
import statistics
import csv

#_________________________________________________________________________________
# OVERALL RANK UNIVERSITY RANK ALL OF STUDENTS OF THAT PARTICULAR SEM GENRATOR!!

with open('./extracted_data_json/results.json') as fl:
    DATA = json.loads(fl.read())

allStudents, SORTED_DATA, INFO = [], [] ,{}

for branch in DATA.keys():
    for student in DATA[branch]:
        allStudents.append(student)

SORTED_DATA = sorted(allStudents, key=lambda x: ( -float(x['sgpa']) , x['name'])) #- Represents descending order!!

for i, stud in enumerate(SORTED_DATA):
    stud['rank'] = i+1

# sdata = sorted(allStudents, key=lambda x: x['sgpa'], reverse=True) FOR SORTING BY SGPA ONLY IN DESCENDING
# TO UNDERSTAND THIS LINE AS THIS LINE SLOVED YOUR WHOLE CODE LOGIC IS UNDER THIS LINE!!
# LAMDA FUNCTION , SORTED FUNCTION REAL POWER OF PYTHON

with open('./extracted_data_json/uniwise_ranked_results.json', 'w') as fl:
    fl.write(json.dumps(SORTED_DATA, indent=4))


# SETTING UP A CSV FILE FOR SAME DATA ________________________________________________________
data_file = open('./ranked_results_csv/1_UNI_ranked_results.csv', 'w')
csv_writer = csv.writer(data_file)

count = 0
for stud in SORTED_DATA:
    if count == 0:
        # Writing headers of CSV file
        header = ['RANK', 'NAME', 'ROLL NO.', 'CREDITS', 'SGPA']
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow([stud['rank'], stud['name'], stud['rolln'], stud['credits'], stud['sgpa']])

data_file.close()
#___________________________________________________________________________________________________


cg_list = []
for stud in allStudents:
    cg_list.append(float(stud['sgpa']))

# UNIVERSITY CG STATISTICS
INFO['UNI'] = {
        'Average': statistics.mean(cg_list),
        'Median': statistics.median(cg_list),
        'Mode': statistics.mode(cg_list),
        'Highest': max(cg_list),
        'Lowest': min(cg_list)
    }

#_________________________________________________________________________________
# BRANCH WISE STUDENT SORTING BRANCH WISE RANKING

for branch in DATA.keys():
    branch_students = DATA[branch]
    branch_students = sorted(branch_students, key=lambda x: ( -float(x['sgpa']) , x['name']))
    for i, stud in enumerate(branch_students):
        stud['rank'] = i + 1
    DATA[branch] = branch_students

    cg_list_branchwise = []
    for stud in DATA[branch]:
        cg_list_branchwise.append(float(stud['sgpa']))

    INFO[branch] = {
        'Average': statistics.mean(cg_list_branchwise),
        'Median': statistics.median(cg_list_branchwise),
        'Mode': statistics.mode(cg_list_branchwise),
        'Highest': max(cg_list_branchwise),
        'Lowest': min(cg_list_branchwise)

    }

with open('./extracted_data_json/branchwise_ranked_results.json', 'w') as fl:
    fl.write(json.dumps(DATA, indent=4))

with open('./extracted_data_json/cg_analysis.json', 'w') as fl:
    fl.write(json.dumps(INFO, indent=3))

#_________________________________________________________________________________

for branch in DATA.keys():

    data_file = open(f'./ranked_results_csv/{branch}_ranked_results.csv', 'w')
    csv_writer = csv.writer(data_file)
    count = 0

    for stud in DATA[branch]:

        if count == 0:
            # Writing headers of CSV file
            header = ['RANK', 'NAME', 'ROLL NO.', 'CREDITS', 'SGPA']
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow([stud['rank'], stud['name'], stud['rolln'], stud['credits'], stud['sgpa']])

    data_file.close()


#__________________________________CG ANALYSIS CSV BRANCHWISE AND UNIWISE BOTH_________________________________________

data_file = open('./ranked_results_csv/cg_analysis.csv', 'w')
csv_writer = csv.writer(data_file)

count = 0
for branch in INFO:
    if count == 0:
        # Writing headers of CSV file
        header = ['BRANCH',  'Highest', 'Average' ,'Your', 'Median', 'Max Appeared', 'Lowest']
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow([branch, INFO[branch]['Highest'],round(INFO[branch]['Average'], 2),None,INFO[branch]['Median'], INFO[branch]['Mode'], INFO[branch]['Lowest']])

data_file.close()

#___________________________________________________________________________
