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


driver.get('https://www.collegepravesh.com/engineering-colleges/dtu-delhi/')
time.sleep(3)

# data_file = open('./placement_data/percentage_placed23.csv', 'w')
# csv_writer = csv.writer(data_file)
# percentplace_tb  = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[1]/div[1]/div[2]/table/tbody/tr')
# for i , row in enumerate(percentplace_tb):
#     elemnts = row.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[1]/div[1]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()
#
#
data_file = open('./placement_data/highest_package23.csv', 'w')
csv_writer = csv.writer(data_file)
highestplace_Tb = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr')
for i , row in enumerate(highestplace_Tb):
    elemnts = row.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[{i+1}]/td')
    csv_writer.writerow([elemnts[0].text, elemnts[1].text])
data_file.close()
#
# data_file = open('./placement_data/average_package23.csv', 'w')
# csv_writer = csv.writer(data_file)
# averageplace_tb = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[1]/div[3]/div[2]/table/tbody/tr')
# for i , row in enumerate(averageplace_tb):
#     elemnts = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[1]/div[3]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()


# driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/ul/li[2]").click()
# driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[2]').click()

# data_file = open('./placement_data/percentage_placed22.csv', 'w')
# csv_writer = csv.writer(data_file)
# percentplace_tb  = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr')
# for i , row in enumerate(percentplace_tb):
#     elemnts = row.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()
#
#
# data_file = open('./placement_data/highest_package22.csv', 'w')
# csv_writer = csv.writer(data_file)
# highestplace_Tb = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[2]/div/div[5]/div[2]/table/tbody/tr')
# for i , row in enumerate(highestplace_Tb):
#     elemnts = row.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[2]/div/div[5]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()
#
# data_file = open('./placement_data/average_package22.csv', 'w')
# csv_writer = csv.writer(data_file)
# averageplace_tb = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[2]/div/div[6]/div[2]/table/tbody/tr')
# for i , row in enumerate(averageplace_tb):
#     elemnts = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[2]/div/div[6]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()

# time.sleep(2)
# driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[4]').click()
#
# data_file = open('./placement_data/percentage_placed21.csv', 'w')
# csv_writer = csv.writer(data_file)
# percentplace_tb  = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[4]/div/div[1]/div[2]/table/tbody/tr')
# for i , row in enumerate(percentplace_tb):
#     elemnts = row.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[4]/div/div[1]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()
#
#
# data_file = open('./placement_data/highest_package21.csv', 'w')
# csv_writer = csv.writer(data_file)
# highestplace_Tb = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[4]/div/div[4]/div[2]/table/tbody/tr')
# for i , row in enumerate(highestplace_Tb):
#     elemnts = row.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[4]/div/div[4]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()
#
# data_file = open('./placement_data/average_package21.csv', 'w')
# csv_writer = csv.writer(data_file)
# averageplace_tb = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[4]/div/div[5]/div[2]/table/tbody/tr')
# for i , row in enumerate(averageplace_tb):
#     elemnts = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[2]/div[2]/article/div/div[2]/div[19]/div[2]/div/div[2]/div[4]/div/div[5]/div[2]/table/tbody/tr[{i+1}]/td')
#     csv_writer.writerow([elemnts[0].text, elemnts[1].text])
# data_file.close()


driver.get('https://www.shiksha.com/university/dtu-delhi-technological-university-23920/placement')

time.sleep(3)

datatb = driver.find_elements(By.XPATH,'/html/body/div[3]/main/div/section/div/div[3]/div[1]/div/section[1]/div/div/div/div/div[2]/div/table[2]/tbody/tr')
for row in datatb:
    print(row.text)

