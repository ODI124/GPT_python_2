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

no = input("번호 : ")
name = input("이름 : ")
age = input("나이 : ")

params = {
    "no" : no,
    "name" : name,
    "age" : age,
}
try:
    with conn.cursor() as cursor:
        sql = " UPDATE 학생 "\
            + "SET name = %(name)s "\
            +"     ,age = %(age)s "\
            +" WHERE no = %(no)s "
            
        result = cursor.execute(sql, params)           # DB에 쿼리 요청
        print('{}행의 데이터 수정 완료'.format(result))

    # 변경사항 적용
    conn.commit()
except pymysql.MySQLError as e:
    print('MySQL 에러 : ', e)
finally:
    conn.close()
