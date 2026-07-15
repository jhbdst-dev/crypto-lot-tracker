import psycopg2

# DB 연결
def connect_db():
    
    return psycopg2.connect(
        dbname="crypto_lot_tracker",
        user="hs",
        host="localhost",
        port="5432"
    )

def get_trades():

    # DB 연결
    conn = connect_db()

    # SQL 실행 준비
    cur = conn.cursor()

    # SQL 실행
    cur.execute("SELECT * FROM trades")

    # 결과 가져오기
    rows = cur.fetchall()

    # 정리
    cur.close()
    conn.close()

    return rows

def save_trades(trades):
    
    # DB 연결
    conn = connect_db()

    # SQL 실행 준비
    cur = conn.cursor()

    # 거래 하나씩 저장
    for trade in trades:
        pass