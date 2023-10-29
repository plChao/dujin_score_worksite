import numpy as np
import pandas as pd
import random

random_number_list = [random.randint(0, 5310) for _ in range(1000)]

df = pd.read_csv('../2024_table/actual_exam_situation.csv')

print(len(df))
for index, row in df.iterrows():
    if index in random_number_list:
        df.loc[index, 'correctness_minus'] = int(10)
    else:
        df.loc[index, 'correctness_minus'] = int(0)
df.to_csv('./mimic_result_of_quiz.csv', index=False)