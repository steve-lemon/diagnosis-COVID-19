from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re

country_patients_num = pd.read_csv("./country/country_patients_num.csv")

france_data = country_patients_num[country_patients_num['siteid'] == "France"]
germany_data = country_patients_num[country_patients_num['siteid'] == "Germany"]
italy_data = country_patients_num[country_patients_num['siteid'] == "Italy"]
usa_data = country_patients_num[country_patients_num['siteid'] == "USA"]

france_group = france_data['num_patients'].groupby(france_data['group_name'])
france_desc_sort_result = france_group.sum().to_frame().reset_index().sort_values(by='num_patients', ascending=False)
france_result = france_desc_sort_result.head(10)
print(france_result)
france_result.to_csv('./result/country_france_top10_icd_name.csv', index=True, encoding="UTF-8")

germany_group = germany_data['num_patients'].groupby(germany_data['group_name'])
germany_desc_sort_result = germany_group.sum().to_frame().reset_index().sort_values(by='num_patients', ascending=False)
germany_result = germany_desc_sort_result.head(10)
print(germany_result)
germany_result.to_csv('./result/country_germany_top10_icd_name.csv', index=True, encoding="UTF-8")

italy_group = italy_data['num_patients'].groupby(italy_data['group_name'])
italy_desc_sort_result = italy_group.sum().to_frame().reset_index().sort_values(by='num_patients', ascending=False)
italy_result = italy_desc_sort_result.head(10)
print(italy_result)
italy_result.to_csv('./result/country_italy_top10_icd_name.csv', index=True, encoding="UTF-8")

usa_group = usa_data['num_patients'].groupby(usa_data['group_name'])
usa_desc_sort_result = usa_group.sum().to_frame().reset_index().sort_values(by='num_patients', ascending=False)
usa_result = usa_desc_sort_result.head(10)
print(usa_result)
usa_result.to_csv('./result/country_usa_top10_icd_name.csv', index=True, encoding="UTF-8")
