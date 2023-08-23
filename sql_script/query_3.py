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
# 考生 id
exam_id_of_student = '2023T06001'
# query: 該考生的考試段數 id 與最後評分老師
query = f'select article_id, final_examiner from actual_exam_situation where exam_id = "{exam_id_of_student}"'
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
