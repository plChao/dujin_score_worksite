import numpy as np
import pandas as pd

df = pd.read_csv('./第三屆中華文化經典會考-【道親】報名表 (回覆) - 經典獎內容表.csv')
awards_df = pd.DataFrame()
for col in df.columns:
    filter_col = col.replace(' ', '')
    data_dict = {'award_id': filter_col[:4], 'article_id': '', 'award_name': filter_col[4:]}
    for content in list(df[col]):
        if str(content) == 'nan':
            continue
        print(content)
        data_dict['article_id'] = content[:4]
        awards_df = awards_df.append(data_dict, ignore_index=True)
    print(list(df[col]))
awards_df.to_csv('../2024_table/awards.csv', index=False)
