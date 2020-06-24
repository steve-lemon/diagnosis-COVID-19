#-*- coding:utf-8 -*-
ignore_kor_symptom = {"Empty Icd Name"}

def isIgnoreSymptom(str):
	if str in ignore_kor_symptom:
		return True
	else:
		return False

def getWeight(num, isWeight):
	if not isWeight:
		return 1

	if 0 <= num < 50:
		return 1
	elif 50 <= num < 100:
		return 2
	elif 100 <= num < 500:
		return 5
	elif 500 < num <= 1000:
		return 10
	else:
		return 30
