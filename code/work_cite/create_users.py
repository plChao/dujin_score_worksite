import pandas as pd
from django.contrib.auth.models import User
from .models import *

import pandas as pd
from django.db import IntegrityError


def create_user():
    # 根據報名資訊建立評鑑老師帳號
    teachers = all_examinee_info.objects.filter(job='評鑑老師')

    account_data = [
        {
            'username': teacher.exam_id,
            'password': 'a0' + str(teacher.personal_phone_number),
            'last_name': teacher.name
        }
        for teacher in teachers
    ]

    account_df = pd.DataFrame(account_data)

    for index, row in account_df.iterrows():
        try:
            User.objects.create_user(**row)
        except IntegrityError:
            pass

    print("建立使用者完畢 !")

    account_df.to_csv('create_account.csv', index=False)

def run():
    create_user()