RESULTS = {}
import pdfplumber
import json, os

listdir = os.listdir('./result_data_pdf/')
for result_file in listdir:

    with pdfplumber.open(f'result_data_pdf/{result_file}') as pdf:
        count = 1
        RESULTS[result_file.replace('.pdf', '')] = []
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:

                    if len(row) == 12:
                        error=-1
                    elif len(row) == 14:
                        error=+1
                    else:
                        error=0

                    if (row[0] == str(count)):

                        if len(row) > 11 and row[10+error] != '0':

                            RESULTS[result_file.replace('.pdf', '')].append(
                                {
                                    'name': row[2],
                                    'rolln': row[1],
                                    'credits': row[10 + error],
                                    'sgpa': row[9 + error],
                                    's_no': row[0]
                                }
                            )

                        count +=1

with open('./extracted_data_json/results.json', 'w') as fl:
    fl.write(json.dumps(RESULTS, indent=3))

# print(f'{row[0]}. NAME: {row[2]} {row[1]} ! CREDITS: {row[10 + error]} SGPA: {row[9 + error]}')