#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re
import common_fuc as ignore
from time import sleep

chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)

depth1 = range(1, 23)
depth2 = range(1, 30)
depth3 = range(1, 30)

# depth1 = range(1, 4)
# depth2 = range(1, 3)
# depth3 = range(1, 10)

icd_code = list()
icd_kor_name = list()

for i in depth1:
	for j in depth2:
		url_param = str(i) + "." + str(j) + "&n"
		url = "http://www.koicd.kr/2016/kcd/v7.do#" + url_param
		driver.get(url)
		sleep(1)
		html = driver.page_source
		s1 = BeautifulSoup(html, 'html.parser')
		for k in depth3:
			id = str(i) + "." + str(j) + "." + str(k) + "_anchor"
			print(id)
			try:
				a1 = s1.find("a", {"id": id}).text
				a2 = a1.split(" ")
				print(a1)
				icd_code.append(a1[:3])
				icd_kor_name.append(a1[4:])
			except AttributeError as ex:
				continue

d = {}
d['icd_code'] = icd_code
d['icd_kor_name'] = icd_kor_name

icd_dict = pd.DataFrame(d)

print(icd_dict)
icd_dict.to_csv("./data2/icd_kor_mapping.csv", index=True, encoding="UTF-8")
