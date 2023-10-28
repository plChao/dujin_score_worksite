import pandas as pd

df_clean = pd.read_csv('./第三屆中華文化經典會考_道親_表單回應 1.csv')

# 留下最新資料
df_clean = df_clean.sort_values(by=['時間戳記'],ascending=False)
df_clean_2 = df_clean.drop_duplicates(subset='姓名') 

# 處理佛堂編號
df_clean_2 = df_clean_2.fillna("")
df_clean_2['tan'] = df_clean_2['佛堂1-1'] + df_clean_2['佛堂1-2'] + df_clean_2['佛堂1-3'] + df_clean_2['佛堂2-1'] + df_clean_2['佛堂2-2'] + df_clean_2['佛堂2-3'] + df_clean_2['佛堂名']
# print(df_clean_2.iloc[1])
df_clean_2['tan_id'] = [ x[:3] for x in df_clean_2['tan']] 
df_clean_2['tan_name'] = [ x[3:] for x in df_clean_2['tan']] 
df_clean_2['SerialNumber'] = df_clean_2.groupby(['tan_id']).cumcount() + 1
df_clean_2['SerialNumber'] = df_clean_2['SerialNumber'].astype(str).str.zfill(3)
df_clean_2['exam_id'] = '2023' + df_clean_2['tan_id'] + df_clean_2['SerialNumber']

df_all = df_clean_2[['姓名','性別','報考人電話','連絡人','連絡人電話', '請留下e-mail','tan_id', 'exam_id','tan_name']]
df_type = pd.read_csv('./第三屆考官分組查詢 - 考生.csv')
print('df_all', len(df_all), 'df_quiz_time', len(df_type))
df_all_time = df_all.merge(df_type, how='left')
print(df_all_time.shape)
rename_dict = {
    '姓名':'name',
    '性別':'gender',
    '報考人電話':'personal_phone_num',
    '連絡人':'contact_person',
    '連絡人電話':'contact_person_num',
    '請留下e-mail':'email',
    '工作別':'job',
    '考試時間':'exam_date',
    '考試組別':'exam_group'
}
df_all_time = df_all_time.drop(['段數', '准考證號碼'],axis=1)
df_all_time.rename(columns=rename_dict, inplace=True)
df_all_time['signed'] = ""      # 報到欄位
df_all_time['finished'] = ""    # 是否考完

df_all_time.to_csv('../2024_table/all_examinee_info.csv', index=False)
