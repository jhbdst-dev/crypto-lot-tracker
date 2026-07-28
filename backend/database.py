import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL 데이터베이스 연결
def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )

# DB에 저장된 전체 거래내역 조회
def get_trades():

    # DB 연결
    conn = connect_db()

    # SQL 실행 객체 생성
    cur = conn.cursor()

    # trades 테이블 전체 거래내역 조회
    cur.execute("SELECT * FROM trades")

    # 조회 결과 전체 가져오기
    rows = cur.fetchall()

    # SQL 실행 객체와 DB 연결 종료
    cur.close()
    conn.close()

    # 전체 거래내역 반환
    return rows

# 업비트 거래내역을 DB에 저장
def save_trades(trades):

    # DB 연결
    conn = connect_db()

    # SQL 실행 객체 생성
    cur = conn.cursor()

    # 거래내역을 하나씩 확인하며 저장
    for trade in trades:

        # 체결 수량이 없는 주문은 저장하지 않음
        if trade["executed_volume"] == "0":
            continue

        # 거래내역을 trades 테이블에 저장
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

    # 저장한 거래내역을 DB에 최종 반영
    conn.commit()

    # SQL 실행 객체와 DB 연결 종료
    cur.close()
    conn.close()

# DB에 저장된 가장 최근 거래 시간 조회
def get_last_trade_time():

    # DB 연결
    conn = connect_db()

    # SQL 실행 객체 생성
    cur = conn.cursor()

    # trades 테이블에서 가장 최근 거래 시간 조회
    cur.execute(
        """
        SELECT MAX(created_at)
        FROM trades
        """
    )

    # 조회 결과에서 최근 거래 시간 가져오기
    last_trade_time = cur.fetchone()[0]

    # SQL 실행 객체와 DB 연결 종료
    cur.close()
    conn.close()

    # 가장 최근 거래 시간 반환
    return last_trade_time