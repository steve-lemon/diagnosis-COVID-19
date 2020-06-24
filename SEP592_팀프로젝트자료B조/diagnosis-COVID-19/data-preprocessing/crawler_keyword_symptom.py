﻿#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re

merge_data = pd.read_csv('./data2/my-icd-major-patients.csv')
icd_keyword = pd.read_csv('./data2/icd_keyword_mapping.csv')

chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)

symptomList = []

for index, row in merge_data.iterrows():
	a = icd_keyword[icd_keyword['icd_code'] == row['icd_code']]
	keyword = a.get_value(a.index[0], 'keyword')
	if str(keyword) == "nan":
		symptomList.append("Empty Icd Name")
		continue

	symptomSet = set()

	url = "http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseList.do?searchKeyword=" + keyword
	driver.get(url)
	try:
		wait = WebDriverWait(driver, 10)
		element = wait.until(EC.element_to_be_clickable((By.ID, 'footerWrap')))
	except:
		driver.get(url)
		wait = WebDriverWait(driver, 10)
		element = wait.until(EC.element_to_be_clickable((By.ID, 'footerWrap')))

	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	try:
		a_tag_list = soup.findAll("a", href=re.compile("symptomId"))
		print(a_tag_list)

		# 한번이라도 검색 결과가 있으면 return!!!
		for n in a_tag_list:
			print(n.text.strip())
			symptomSet.add(n.text.strip())

	except Exception as ex:
		print(ex)
		# symptomList.append("error_data")
	print("-----------------------------")
	print(symptomSet)
	print("-----------------------------")
	symptomList.append('||'.join(symptomSet))


merge_data['symptom'] = symptomList

# data['inclusion'] = inclusion
# data['exclusion'] = exclusion
merge_data.to_csv('./data2/my-icd-major-patients-symptom.csv', index=True, encoding="UTF-8")