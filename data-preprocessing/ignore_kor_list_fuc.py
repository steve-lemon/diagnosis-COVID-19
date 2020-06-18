#-*- coding:utf-8 -*-
ignore_kor_list = {"기타","및"}

def isIgnore(str):
	if str in ignore_kor_list:
		return True
	else:
		return False
