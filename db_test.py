import psycopg2

# DB 연결
conn = psycopg2.connect(
    dbname="crypto_lot_tracker",
    user="hs",
    host="localhost",
    port="5432"
)

# SQL 실행 준비
cur = conn.cursor()

# SQL 실행
cur.execute("SELECT * FROM trades")

# 결과 가져오기
rows = cur.fetchall()

# 출력
for row in rows:
    print(row)

# 정리
cur.close()
conn.close()