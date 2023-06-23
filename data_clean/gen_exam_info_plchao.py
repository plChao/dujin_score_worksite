import numpy as np
import pandas as pd

df = pd.read_csv('./1_examiner.csv')

order_df = pd.DataFrame()
for index, row in df.iterrows():
    choose_col = [x for x in df.columns if '時間組別' in x]
    for col in choose_col:
        if pd.notna(row[col]):
            row_dict = {
                'examiner_name': row['考官姓名'],
                'exam_date': col[:1],
                'exam_group': row[col]
            }
            order_df = order_df.append(row_dict, ignore_index=True)
order_df['exam_group'] = order_df['exam_group'].astype(int)
order_df.to_csv('exam_info.csv', index=False)