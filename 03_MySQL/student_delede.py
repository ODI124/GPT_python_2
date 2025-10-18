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



try:
    with conn.cursor() as cursor:
        sql = " DELETE FROM 학생 "\
            +" WHERE no = %s "
            
        result = cursor.execute(sql, no)            # DB에 쿼리 요청
        print('{}행의 데이터 삭제 완료'.format(result))

    # 변경사항 적용
    conn.commit()
except pymysql.MySQLError as e:
    print('MySQL 에러 : ', e)
finally:
    conn.close()
