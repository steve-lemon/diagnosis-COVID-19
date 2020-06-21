#-*- coding:utf-8 -*-
import pandas as pd

from collections import Counter
import common_fuc

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import matplotlib
from matplotlib import rc

rc('font', family='NanumBarunGothic')

merge_data = pd.read_csv('./data2/my-icd-major-patients-symptom.csv')
symptom_list = []

for index, row in merge_data.iterrows():
	# print(row['symptom'])
	row_symptom_list = str(row['symptom']).split("||")
	weight = row['sum']
	print("weight=" + str(weight))
	for word in row_symptom_list:
		if common_fuc.isIgnoreSymptom(str(word)):
			continue
		num = 1
		while num <= weight:
			print(num)
			symptom_list.append(word)
			num = num+1

print(len(symptom_list))

counts = Counter(symptom_list)
tags = counts.most_common(1000)

top20 = pd.DataFrame(tags)

top20.to_csv('./result/symptom_result_just_patient.csv', index=True, encoding="UTF-8")


# WordCloud 한글 깨짐. 현상 발생. 주석처리.
# wc = WordCloud(font_path='/Library/Fonts/NanumBarunGothic.ttf', background_color='white', width=800, height=600)
# cloud = wc.generate_from_frequencies(dict(tags))
# plt.figure(figsize=(10, 8))
# plt.axis('off')
# plt.imshow(cloud)
# plt.show()

