import pandas as pd
import tqdm

df_clean = pd.read_csv('./第二屆經典會考-讀經班報名表副本 - 表單回應 1.csv')

# 留下最新資料
df_clean = df_clean.sort_values(by=['時間戳記'],ascending=False)
df_clean_2 = df_clean.drop_duplicates(subset='姓名') 

df_clean_2 = df_clean_2[['姓名','A 基礎道學','B 啟蒙文學','C 古文詩詞選','D 三教經典','E 白陽經典','F 仙佛聖訓','G 仙佛聖訓','H 善歌','經典獎']]
# 得到全部的段
df_clean_2 = df_clean_2.fillna("")
df_clean_2['seg'] = df_clean_2['A 基礎道學'] + ',' + df_clean_2['B 啟蒙文學'] + ','  + df_clean_2['C 古文詩詞選'] + ',' + df_clean_2['D 三教經典'] + ','  + df_clean_2['E 白陽經典']+ ','  + df_clean_2['F 仙佛聖訓']+ ','  + df_clean_2['G 仙佛聖訓']+ ','  + df_clean_2['H 善歌']
# print(df_clean_2.iloc[1]['seg'])

df = pd.DataFrame()
for index, row in tqdm.tqdm(df_clean_2.iterrows(),total=len(df_clean_2)):
    new_str = row['seg'].replace(" ", "")
    for x in new_str.split(','):
        if len(x) > 0:
            df = df.append({'name': row['姓名'], 'article_id': x[0:4]}, ignore_index=True)
print(df)
df['correctness_minus'] = ""
df['fluency_minus']=""
df['final_score']=""
df['final_examiner']=""
df['score_id']=""
df_type = pd.read_csv('../2023_table/all_examinee_info.csv')[['name', 'exam_id']]
print('df', len(df), 'df_examinee', len(df_type))
df = df.merge(df_type, how='left')
output_csv = '../2023_table/actual_exam_situation.csv'
import os
if os.path.exists(output_csv):
    previous_df = pd.read_csv(output_csv)
    df = pd.concat([previous_df, df])
print(len(df), len(df.drop_duplicates(keep=False)))
df = df.drop_duplicates()
df.to_csv(output_csv, index=False)
