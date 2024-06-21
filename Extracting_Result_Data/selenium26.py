from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import time
import json

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(7)
brnch = {'ENE': 'EN',
         'EP': 'EP',
         'COE': 'CO',
         'BT': 'BT',
         'SE': 'SE',
         'MCE': 'MC',
         'PIE': 'PE',
         'CHE': 'CH',
         'CE': 'CE',
         'ME':'ME',
         'MAM': 'AE',
         'ECE': 'EC',
         'IT': 'IT',
         'EE': 'EE',
         'Cumulative':'UNI'}

try:
    driver.get('https://www.resulthubdtu.com/DTU/Results/2026')
    time.sleep(3)

    brnchbuttons = driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/button')
    for j, branchbt in enumerate(brnchbuttons):
        # if j==0:
        #     continue

        branchbt.click()
        time.sleep(1)
        brnch_name = str(branchbt.text).strip()
        print(brnch[brnch_name])

        tb_rows = driver.find_elements(By.XPATH, r'/html/body/div/div/div[2]/div/div[3]/div/div/div[2]/table/tbody/tr')

        data_file = open(f'./ranked_results_csv/26_{brnch[brnch_name]}_ranked_results.csv', 'w')
        csv_writer = csv.writer(data_file)

        for i , tb_row in enumerate(tb_rows):

            if i==0:
                header = ['RANK', 'NAME', 'ROLL NO.', 'SEM1', 'SEM2', 'SEM3', 'Cumulative CGPA']
                csv_writer.writerow(header)
                continue

            elements = tb_row.find_elements(By.CLASS_NAME, "px-3.py-2")

            #_ ROLL NUMBER ACHEE SE KAR RHA
            if len(elements[2].text.strip())==10:
                ROLLNO = (elements[2].text)[2:7] + '/0' + (elements[2].text)[8:]
            else:
                ROLLNO = (elements[2].text).replace('2K', '')

            csv_writer.writerow([elements[0].text,elements[1].text,ROLLNO,elements[3].text,elements[4].text,elements[5].text,elements[6].text])


        data_file.close()

except Exception as e:
    print(e)


