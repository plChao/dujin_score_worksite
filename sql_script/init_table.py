
import mysql.connector
 
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)
 
cursor = mydb.cursor()

# 製作 db
cursor.execute("CREATE DATABASE geeksforgeeks")
# 匯入表格

# 算時間
