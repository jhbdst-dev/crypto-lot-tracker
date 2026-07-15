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
            ON CONFLICT (uuid) DO NOTHING
            """,
            (
                trade["uuid"],
                trade["market"],
                trade["side"],
                trade["ord_type"],
                trade["state"],
                trade.get("price"),
                trade.get("volume"),
                trade["executed_volume"],
                trade["executed_funds"],
                trade["paid_fee"],
                trade.get("trades_count", 0),
                trade["created_at"],
            )            
        )

    conn.commit()

    cur.close()
    conn.close()

def get_last_trade_time():
    # DB 연결
    conn = connect_db()

    # SQL 실행 준비
    cur = conn.cursor()

    # 가장 최근 거래 시간 조회
    cur.execute(
        """
        SELECT MAX(created_at)
        FROM trades
        """
    )

    last_trade_time = cur.fetchone()[0]

    cur.close()
    conn.close()

    return last_trade_time