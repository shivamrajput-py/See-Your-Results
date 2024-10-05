import pdfplumber
import json, os, csv
import pandas as pd

scrapelist = ['E24_BTECH_PE_SE_CS_EP_EC_ME_II_1733.pdf', 'E24_BTECH_AE_CH_BT_CE_EE_II_1733.pdf']

def csv_to_json(csv_file_path, json_file_path):
    data = []

    # Open the CSV file and load data into a list of dictionaries
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    # Write the list of dictionaries to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

#   2027    ------------------------------------------------------------------------------------------------------------------------------

# MAIN RECENT SEMESTER (2) (2027 BATCH) RESULTS FROMATOR UNIVERSITY LEVEL
if False:

    result = []

    scrapelist = os.listdir('./result_data_pdf')
    for result_file in scrapelist:
        if 'E24' not in str(result_file):
            continue

        pdf = pdfplumber.open(f'result_data_pdf/{result_file}')
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:

                    if str(row[0]).isnumeric():

                        if len(row)<11:
                            continue
                        else:
                            error = len(row)-12

                        result.append({
                            "NAME": row[2],
                            "ROLL NO.": row[1],
                            "CREDITS2": row[-2],
                            "SGPA2": row[-3],
                            "GRADE2": row[3:-3],
                            "S_NO": row[0]
                        })


    pdf.close()
    open('./ranked_results_csv/recentSemData.json', 'w').write(json.dumps(result, indent=3))

#---------------------------------------------------------------------------------------------------------------------------------------

# OLD SEMEMSTER RESULT SEM 1 (2027 BATCH) RESULT FORMATOR WITH GRADE
if False:
    result = []

    scrapelist = os.listdir('./result_data_pdf')
    for result_file in scrapelist:
        count = 1
        if 'E24' in str(result_file):
            continue

        pdf = pdfplumber.open(f'result_data_pdf/{result_file}')

        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:

                    if '23/' in str(row[1]):

                        if len(row)<11:
                            continue
                        else:
                            error = len(row)-12

                        result.append({
                            "ROLL NO.": row[1],
                            "CREDITS1": row[-3],
                            "SGPA1": row[-4],
                            "GRADE1": row[3:-4],
                            "S_NO": row[0]
                        })
                        count += 1

    open('./ranked_results_csv/prevSemData.json', 'w').write(json.dumps(result, indent=3))

#------------------------------------------------------------------------------------------------------------------------------

# MERGING BOTH SEM 1 AND SEM 2 RESULTS WITH EACH OTHER FOR MAIN FINAL CSV
if False:

    main_json = json.loads(open('./ranked_results_csv/recentSemData.json', 'r').read())
    mergedata_json = json.loads(open('./ranked_results_csv/prevSemData.json', 'r').read())

    fl = open('./ranked_results_csv/27Batch_allStudent.csv', 'w')
    FINALDF = csv.writer(fl)
    FINALDF.writerow(['RANK','NAME','ROLL NO.','CREDITS1','SGPA1','GRADE1','CREDITS2','SGPA2','GRADE2', 'CUMULATIVE CGPA','S_NO'])

    for student in main_json:
        for stud in mergedata_json:

            if stud['ROLL NO.'] == student['ROLL NO.']:
                cum_cg = round((float(stud['SGPA1']) + float(student['SGPA2']))/2, 3)
                FINALDF.writerow([1, student['NAME'], student['ROLL NO.'],
                                  stud['CREDITS1'], stud['SGPA1'], stud['GRADE1'],
                                  student['CREDITS2'], student['SGPA2'], student['GRADE2'],
                                  cum_cg, student['S_NO']])


    fl.close()

    mncsv = pd.read_csv("./ranked_results_csv/27Batch_allStudent.csv")
    mncsv = mncsv.sort_values(by= [mncsv.columns[-2], mncsv.columns[1]], ascending=[False, True])
    mncsv.to_csv('./ranked_results_csv/27Batch_allStudent.csv', index=False)


#    2026   ---------------------------------------------------------------------------------------------------------------------------------------

if True:

    result = []
    scrapelist = ['26Batch_SEM4_AE_BT_CH_EE_EN_EP_IT_MC_PE_SE_IV_1734.pdf']

    for result_file in scrapelist:

        pdf = pdfplumber.open(f'result_data_pdf/{result_file}')
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:

                    if str(row[0]).isnumeric():

                        if len(row) < 11:
                            continue
                        else:
                            error = len(row) - 12

                        result.append({
                            "NAME": row[2],
                            "ROLL NO.": row[1],
                            "CREDITS4": row[-2],
                            "SGPA4": row[-3],
                            "GRADE4": row[3:-3],
                            "S_NO": row[0]
                        })

    pdf.close()
    open('./ranked_results_csv/26B_sem4.json', 'w').write(json.dumps(result, indent=3))

    csv_to_json('./ranked_results_csv/26Batch_allStudent.csv', './ranked_results_csv/26Batch_allStudent.json')

    main_json = json.loads(open('./ranked_results_csv/26Batch_allStudent.json', 'r').read())
    mergedata_json = json.loads(open('./ranked_results_csv/26B_sem4.json', 'r').read())

    fl = open('./ranked_results_csv/UNI_rankedR26.csv', 'w')
    FINALDF = csv.writer(fl)
    FINALDF.writerow(['RANK','NAME','ROLL NO.','SGPA1','SGPA2','SGPA3','SGPA4','CREDITS4','GRADE4' ,'CUMULATIVE CGPA'])

    for student in main_json:
        for stud in mergedata_json:
            if '/00' in student['ROLL NO.']: studrn = student['ROLL NO.'].replace('/00', '/0')
            elif '/0' in student['ROLL NO.']: studrn = student['ROLL NO.'].replace('/0', '/')
            else: studrn = student['ROLL NO.']

            if (stud['ROLL NO.'].replace('2K', '')) == (studrn):
                cum_cg = round((float(student['SEM1']) + float(student['SEM2'])+ float(student['SEM3'])+ float(stud['SGPA4']))/4, 3)
                FINALDF.writerow([1, student['NAME'], student['ROLL NO.'],
                                  student['SEM1'], student['SEM2'], student['SEM3'], stud['SGPA4'],
                                  stud['CREDITS4'], stud['GRADE4'],
                                  cum_cg])


    fl.close()

    mncsv = pd.read_csv("./ranked_results_csv/UNI_rankedR26.csv")
    mncsv = mncsv.sort_values(by= [mncsv.columns[-1], mncsv.columns[1]], ascending=[False, True])
    mncsv.to_csv('./ranked_results_csv/UNI_rankedR26.csv', index=False)
