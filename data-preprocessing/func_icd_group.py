# -*- coding:utf-8 -*-
ignore_kor_list = {"기타", "및"}


def get(str):
	if str >= "A00" and str <= "A09":
		return True
	else:
		return False


print(isIgnore("A08"))
print(isIgnore("A10"))
