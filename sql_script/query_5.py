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
# 首頁所需的，純考生報到數量以及考試通過數量
# 以下是報到以及總數的數量
# query = f'SELECT SUM(signed), count(*) from all_examinee_info where job = "純考生"'
# 以下是完成考試的數量
query = f'select count(*) from all_examinee_info \
            JOIN ( \
                SELECT exam_id, SUM(final_score IS NULL) AS unfinish \
                FROM actual_exam_situation GROUP BY exam_id \
            ) AS grade_all \
            ON grade_all.exam_id = all_examinee_info.exam_id \
            WHERE job = "純考生" AND unfinish = 0'
print(query)
start_time = time.time()
# time calculate
cursor.execute(query)

end_time = time.time()
execution_time = end_time - start_time
try:
    column_names = [desc[0] for desc in cursor.description]
    print("Column names:", column_names)
    results = cursor.fetchall()
    for row in results:
        print(row)
except:
    rows_affected = cursor.rowcount
    print(f"Rows affected: {rows_affected}")

print(f"Query execution time: {execution_time:.6f} seconds")

cursor.close()
mydb.close()
