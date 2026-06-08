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

total_quantity = 0
total_buy_amount = 0

# 출력
for row in rows:
    total_quantity += row[5]
    total_buy_amount += row[7]

print(f"총 보유수량: {total_quantity}")
print(f"총 매수금액: {total_buy_amount}")
average_buy_price = total_buy_amount / total_quantity
print(f"평균 매수가: {average_buy_price}")

# 정리
cur.close()
conn.close()