import mysql.connector
import time

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="alan0415",
    database="mydb"
)
cursor = mydb.cursor()
# variables
# 評分老師 id
# query: 老師的考生評分頁面，老師參與的所有考試場次中的參加者的
# exam_id, exam_date, ..., finish_num: 已經評分的段數, article_num: 報名的段數
exam_id_of_teacher = '2023T06001'
query = f'select info.exam_id, exam_date, exam_group, name, tan_name, finish_num, article_num\
      from (SELECT examinee.exam_id, examinee.exam_date, examinee.exam_group, name, tan_name\
    FROM all_examinee_info AS examinee \
    JOIN (SELECT exam_date, exam_group FROM exams WHERE exam_id = "{exam_id_of_teacher}")AS exam_group_table \
    ON examinee.exam_date = exam_group_table.exam_date \
    and examinee.exam_group = exam_group_table.exam_group) as info \
    JOIN (SELECT exam_id, SUM(final_examiner is not null) AS finish_num, count(article_id) AS article_num \
                FROM actual_exam_situation \
                GROUP BY exam_id) as number on info.exam_id = number.exam_id \
    order by exam_date'
# query = f'SELECT examinee.exam_id, examinee.exam_date, examinee.exam_group, name, tan_name\
#     FROM all_examinee_info AS examinee \
#     JOIN (SELECT exam_date, exam_group FROM exams WHERE exam_id = "{exam_id_of_teacher}")AS exam_group_table \
#     ON examinee.exam_date = exam_group_table.exam_date \
#     and examinee.exam_group = exam_group_table.exam_group'
print(query)
start_time = time.time()
# time calculate
cursor.execute(query)

end_time = time.time()
execution_time = end_time - start_time

column_names = [desc[0] for desc in cursor.description]

# Print column names
print("Column names:", column_names)

results = cursor.fetchall()

for row in results:
    print(row)

print(f"Query execution time: {execution_time:.6f} seconds")

cursor.close()
mydb.close()
