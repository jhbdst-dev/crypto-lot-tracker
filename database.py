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

        cur.execute(
            """
            INSERT INTO trades (
                uuid,
                market,
                side,
                ord_type,
                state,
                price,
                volume,
                executed_volume,
                executed_funds,
                paid_fee,
                trades_count,
                created_at
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s
            )
            """,
            (
                trade["uuid"],
                trade["market"],
                trade["side"],
                trade["ord_type"],
                trade["state"],
                trade["price"],
                trade["volume"],
                trade["executed_volume"],
                trade["executed_funds"],
                trade["paid_fee"],
                trade["trades_count"],
                trade["created_at"],
            )
        )

    conn.commit()

    cur.close()
    conn.close()