from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re

data = pd.read_csv('./country/Diagnoses-CombinedByCountry200411.csv')
conut = len(data)
print(conut)
# num_patients >0 && icd_version == 0 만 가져온다.
filter_1 = data[(data['num_patients'] > 0) & (data['icd_version'] == 10)]
country_patients_num = filter_1[['siteid', 'icd_code', 'num_patients']]

#icd_code를 5자리로 자른다. 5자리 보다 크면 검색하기가 어렵다.
country_patients_num['icd_code_1'] = country_patients_num['icd_code'].apply(lambda x: x[:3])
print(country_patients_num)

icd_group = pd.read_csv('./data2/icd_group.csv')
groupNameList = []

for index, row in country_patients_num.iterrows():
	condition = 'icd_from<="' + row['icd_code_1'] + '"<= icd_to'
	print(condition)
	a = icd_group.query(condition)
	if len(a) == 0:
		groupNameList.append("기타")
	else:
		groupNameList.append(a.get_value(a.index[0], 'icd_group_name'))

print(groupNameList)

country_patients_num['group_name'] = groupNameList
country_patients_num.to_csv("./country/country_patients_num.csv", index=True, encoding="UTF-8")

france_data = country_patients_num[country_patients_num['siteid'] == "France"]
germany_data = country_patients_num[country_patients_num['siteid'] == "Germany"]
italy_data = country_patients_num[country_patients_num['siteid'] == "Italy"]
usa_data = country_patients_num[country_patients_num['siteid'] == "USA"]

