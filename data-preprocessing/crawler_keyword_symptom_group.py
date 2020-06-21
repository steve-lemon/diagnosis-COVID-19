#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re

merge_data = pd.read_csv('./data2/my-icd-major-patients-symptom.csv')
icd_group = pd.read_csv('./data2/icd_group.csv')

groupNameList = []

for index, row in merge_data.iterrows():
	condition = 'icd_from<="' + row['icd_code'] + '"<= icd_to'
	print(condition)
	a = icd_group.query(condition)
	if len(a) == 0:
		groupNameList.append("기타")
	else:
		groupNameList.append(a.get_value(a.index[0], 'icd_group_name'))

print(groupNameList)

merge_data['group_name'] = groupNameList
merge_data.to_csv('./data2/my-icd-major-patients-symptom-group.csv', index=True, encoding="UTF-8")
