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
# 限制輸出前十行
query = f'select info.exam_id, info.name, info.pass_num, rank_table.ranking\
            from ( select all_examinee_info.exam_id, all_examinee_info.name, count(*) as pass_num\
                from all_examinee_info, actual_exam_situation \
                WHERE all_examinee_info.exam_id = actual_exam_situation.exam_id and \
                    (tan_id like "T%" or tan_id like "S%") and\
                    final_score > 90\
                group by exam_id, name\
                order by pass_num desc\
            ) as info\
            right join (\
                select row_number() over (order by t.pass_num desc) as ranking, t.pass_num\
                from (select distinct list.pass_num\
                    from (select all_examinee_info.exam_id, all_examinee_info.name, count(*) as pass_num\
                        from all_examinee_info, actual_exam_situation \
                        WHERE all_examinee_info.exam_id = actual_exam_situation.exam_id and \
                            (tan_id like "T%" or tan_id like "S%") and\
                            final_score > 90\
                        group by exam_id, name\
                        order by pass_num desc\
                    ) as list\
                )as t limit 20\
            ) as rank_table on info.pass_num = rank_table.pass_num;'

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
