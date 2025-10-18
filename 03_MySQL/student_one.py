# pip install pymysql
# pip install cryptography
import pymysql

# MySQL 서버에 접속
conn = pymysql.connect(
    host='127.0.0.1',
    user='aloha',
    password='123456',
    database='aloha',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cursor:
        sql = "SELECT * FROM 학생 WHERE no = 1 "
        cursor.execute(sql)             # DB에 쿼리 요청

        student = cursor.fetchone()    # 결과 
        print( student )
except pymysql.MySQLError as e:
    print('MySQL 에러 : ', e)
finally:
    conn.close()
