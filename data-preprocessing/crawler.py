from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re

data = pd.read_csv('./data/diagnoses-combined.csv')
conut = len(data)
print(conut)
# num_patients >0 && icd_version == 0 만 가져온다.
filter_1 = data[(data['num_patients'] > 0) & (data['icd_version'] == 10)]
covid_patients_num = filter_1[['icd_code', 'num_patients']]

#icd_code를 5자리로 자른다. 5자리 보다 크면 검색하기가 어렵다.
covid_patients_num['icd_code'] = covid_patients_num['icd_code'].apply(lambda x: x[:5])
print(covid_patients_num)

icd_code = pd.read_csv('./data/icd-lookup_kor.csv')
print(len(icd_code))

## 필요한 코드만 가져와서 merge 한다.
merge_data = pd.merge(covid_patients_num, icd_code, how='left', on='icd_code')
merge_data.to_csv('./data/merge_raw.csv', index=True, encoding="UTF-8")

merge_data = merge_data[:10]
# print(merge_data)


chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)

# url = "http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseList.do?searchKeyword=" + "격리"
# driver.get(url)
# try:
# 	wait = WebDriverWait(driver, 10)
# 	element = wait.until(EC.element_to_be_clickable((By.ID, 'footerWrap')))
# except:
# 	driver.get(url)
# 	wait = WebDriverWait(driver, 10)
# 	element = wait.until(EC.element_to_be_clickable((By.ID, 'footerWrap')))
#
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# try:
# 	# inclusion_area = soup.find('dt', string="증상").find_next_sibling().find_all('a')
# 	# print(inclusion_area)
# 	inclusion_area = soup.findAll("a", href=re.compile("symptomId"))
# 	inclusion_data = ""
# 	for n in inclusion_area:
# 		inclusion_data = inclusion_data + n.text.strip() + "\n"
# 	print(inclusion_data)
# except Exception as ex:
# 	print(ex)

symptomList = []
for index, row in merge_data.iterrows():

	url = "http://www.amc.seoul.kr/asan/healthinfo/disease/diseaseList.do?searchKeyword=" + str(row['kor_text'])
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
		symptomSet = set([""])
		for n in a_tag_list:
			print(n.text.strip())
			symptomSet.add(n.text.strip())
		print(symptomSet)
		symptomList.append('||'.join(symptomSet))
	except Exception as ex:
		print(ex)
		symptomList.append("error_data")

merge_data['symptom'] = symptomList

# data['inclusion'] = inclusion
# data['exclusion'] = exclusion
merge_data.to_csv('./data/merge_data_symptom.csv', index=True, encoding="UTF-8")
