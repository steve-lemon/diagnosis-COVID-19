#-*- coding:utf-8 -*-
import pandas as pd

merge_data = pd.read_csv('./data2/my-icd-major-patients-group.csv')

grouped = merge_data['sum'].groupby(merge_data['group_name'])

desc_sort_result = grouped.sum().to_frame().reset_index().sort_values(by='sum', ascending=False)

result = desc_sort_result.head(10)

print(result)

result.to_csv('./result/top10_icd_name.csv', index=True, encoding="UTF-8")