#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re
import ignore_kor_list_fuc as ignore
from time import sleep

chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)

depth1 = range(1, 23)
depth2 = range(1, 30)

icd_from = list()
icd_to = list()
icd_mid_name = list()

for i in depth1:
	url = "http://www.koicd.kr/2016/kcd/v7.do#" + str(i) + ".1&n"
	driver.get(url)
	sleep(0.5)
	for j in depth2:
		print(str(i) + "."+str(j))
		html = driver.page_source
		s1 = BeautifulSoup(html, 'html.parser')
		id = str(i) + "." + str(j) + "_anchor"
		try:
			a1 = s1.find("a",{"id":id}).text
			a2 = a1.split(" ")
			print(a2[0])
			print(len(a2[0]))
			if len(a2[0]) == 3:
				icd_from.append(a2[0])
				icd_to.append(a2[0])
				icd_mid_name.append(a1[4:])
			else:
				icd_from.append(a1[:3])
				icd_to.append(a1[4:7])
				icd_mid_name.append(a1[8:])
		except AttributeError as ex:
			continue

d = {}
d['icd_from'] = icd_from
d['icd_to'] = icd_to
d['icd_group_name'] = icd_mid_name

icd_dict = pd.DataFrame(d)

print(icd_dict)
icd_dict.to_csv("./data2/icd_group.csv", index=True, encoding="UTF-8")
