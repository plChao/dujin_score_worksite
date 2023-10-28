import numpy as np
import pandas as pd

df = pd.read_csv('../../../../第三屆_考官分組方式/result/1_examiner.csv')
get_exam_id = pd.read_csv('../2024_table/all_examinee_info.csv')[['exam_id', 'name']]
get_exam_id = get_exam_id.rename(columns = {'name': 'examiner_name'})

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
print(order_df.columns, get_exam_id.columns)
order_df = order_df.merge(get_exam_id, how='left')
order_df.drop(['examiner_name'], axis=1, inplace=True)
order_df.to_csv('../2024_table/exams.csv', index=False)