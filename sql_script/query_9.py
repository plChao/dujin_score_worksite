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
# 壇的通過段數排名
query = f'select tan_name, count(*) as pass_num\
        from all_examinee_info, actual_exam_situation \
        WHERE all_examinee_info.exam_id = actual_exam_situation.exam_id and \
            tan_id like "T%" and\
            final_score > 90\
        group by tan_id, tan_name\
        order by pass_num desc'
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
