#-*- coding:utf-8 -*-
import re
def replaceStr(str):
	a = re.sub("([ㄱ-힣]*)","",str)  # type: str
	return a

print(replaceStr('본태성(원발성)'))