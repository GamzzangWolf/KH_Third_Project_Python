import pymysql

# MySQL 서버 연결
db = pymysql.connect(
    host='127.0.0.1',        # MySQL 서버 주소
    port=3306,               # MySQL 포트 번호
    user='root',             # MySQL 사용자명
    password='1234',         # 비밀번호
    db='teample3',           # 사용하고자 하는 데이터베이스 이름
    charset='utf8'           # 문자셋 설정
)

# 연결이 정상적으로 되면, 이후의 작업을 수행할 수 있습니다.
cursor = db.cursor()
cursor.execute("insert into tag")  # 예시: board 테이블 조회
values = [tagName,normalizedTag]
results = cursor.fetchall()
print(results)

# 연결 종료
cursor.close()
db.close()
