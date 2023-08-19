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
# 單人經典獎
# article_name, award_id, pass_num, cho, qua_num, pass
# exam_id_of_student = '2023T20005'
# query = f'  select award_qualify.article_name, award_qualify.award_id, pass_num, cho, qua_num, (pass_num = award_qualify.qua_num) as pass\
#             from (select article_name, award_id, SUM(final_score is not null and final_score > 90) as pass_num, COUNT(*) as cho \
#             from awards \
#             inner join \
#             (select article_id, final_score from actual_exam_situation \
#             where exam_id = "{exam_id_of_student}") as grade \
#             on grade.article_id = awards.article_id \
#             group by award_id, article_name) as grade_all\
#             inner join \
#             (select article_name, award_id, count(*) as qua_num\
#             from awards\
#             group by award_id, article_name) as award_qualify \
#             on award_qualify.award_id = grade_all.award_id \
#             where award_qualify.qua_num = grade_all.cho;'

# 所有經典獎, 有資格/獲獎
# article_name, exam_id, name, pass_num, cho, qua_num, pass
query = f'select award_qualify.article_name, exam_id, grade_all.name, pass_num, cho, qua_num, (pass_num = award_qualify.qua_num) as pass\
            from (select article_name, award_id, exam_id, name, SUM(final_score is not null and final_score > 90) as pass_num, COUNT(*) as cho \
            from awards \
            inner join \
            (select article_id, final_score, exam_id, name from actual_exam_situation) as grade \
            on grade.article_id = awards.article_id \
            group by award_id, article_name, exam_id, name) as grade_all\
            inner join \
            (select article_name, award_id, count(*) as qua_num\
            from awards\
            group by award_id, article_name) as award_qualify \
            on award_qualify.award_id = grade_all.award_id \
            where award_qualify.qua_num = grade_all.cho\
            order by award_qualify.award_id, exam_id;'
# 所有經典獎, 獲獎者
query = f'select award_qualify.article_name, exam_id, grade_all.name, pass_num, cho, qua_num, (pass_num = award_qualify.qua_num) as pass\
            from (select article_name, award_id, exam_id, name, SUM(final_score is not null and final_score > 90) as pass_num, COUNT(*) as cho \
            from awards \
            inner join \
            (select article_id, final_score, exam_id, name from actual_exam_situation) as grade \
            on grade.article_id = awards.article_id \
            group by award_id, article_name, exam_id, name) as grade_all\
            inner join \
            (select article_name, award_id, count(*) as qua_num\
            from awards\
            group by award_id, article_name) as award_qualify \
            on award_qualify.award_id = grade_all.award_id \
            where award_qualify.qua_num = grade_all.cho and pass_num = award_qualify.qua_num\
            order by award_qualify.award_id, exam_id;'
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
