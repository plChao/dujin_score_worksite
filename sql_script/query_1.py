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
exam_id_of_student = '"2023T06001"'
query = 'SELECT name, article_id, correctness_minus, fluency_minus, \
    final_score, final_examinar FROM actual_exam_situation WHERE exam_id = ' + exam_id_of_student
print(query)
start_time = time.time()
# time calculate
cursor.execute(query)

end_time = time.time()
execution_time = end_time - start_time

results = cursor.fetchall()
for row in results:
    print(row)

print(f"Query execution time: {execution_time:.6f} seconds")

cursor.close()
mydb.close()
