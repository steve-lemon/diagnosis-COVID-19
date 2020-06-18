#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re
import ignore_kor_list_fuc as ignore


merge_data = pd.read_csv('./data2/my-icd-major-patients.csv')

chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)

symptomList = []
for index, row in merge_data.iterrows():

	if str(row['icd_kor']) == "nan":
		symptomList.append("Empty Icd Name")
		continue

	icd_kor_list = list()
	icd_kor_list.append(str(row['icd_kor']))
	# icd_kor_txt = str(row['icd_kor']).split()  # type: List[str]
	# print(icd_kor_txt)
	# for word in icd_kor_txt:
	# 	icd_kor_list.append(word)

	# print (icd_kor_list)
	# print ("---------------")
	symptomSet = set()
	for icd_kor in icd_kor_list:

		if ignore.isIgnore(icd_kor):
			continue

		url = "http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseList.do?searchKeyword=" + icd_kor
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
			if len(a_tag_list) == 0:
				continue
			else:
				for n in a_tag_list:
					print(n.text.strip())
					symptomSet.add(n.text.strip())
				break

			# for n in a_tag_list:
			# 	print(n.text.strip())
			# 	symptomSet.add(n.text.strip())

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
