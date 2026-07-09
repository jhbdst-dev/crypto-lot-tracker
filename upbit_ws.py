import websocket
import json
from decimal import Decimal
from calculator import calculate_asset

def watch_current_price(rows, fee_rate):
    # WebSocket 연결 객체 생성
    ws = websocket.WebSocket()

    # 업비트 서버 연결
    ws.connect("wss://api.upbit.com/websocket/v1")
    print("업비트 WebSocket 연결 완료")

    # 구독 요청
    ws.send('[{"ticket":"test"},{"type":"ticker","codes":["KRW-XRP"]}]')
    print("구독 요청 완료")

    previous_price = None

    while True:
        data = ws.recv()
        # print("데이터 수신")

        data = json.loads(data)
        current_price = Decimal(str(data["trade_price"]))

        if current_price != previous_price:
            (
                total_quantity,
                total_buy_amount,
                average_buy_price,
                current_value,
                profit_loss,
                profit_rate,
                per_trade_results,
                sell_trade_results
            ) = calculate_asset(rows, current_price, fee_rate)
            previous_price = current_price
            
            print("\n" + "=" * 50)
            print("실시간 보유자산")
            print("=" * 50)
            print(f"현재가: {current_price:,.0f}원")
            print(f"총 보유수량: {total_quantity:.8f}")
            print(f"총 매수금액: {total_buy_amount:,.0f}원")
            print(f"평균 매수가: {average_buy_price:,.2f}원")
            print(f"현재 평가금액: {current_value:,.0f}원")
            print(f"평가손익: {profit_loss:,.0f}원")
            print(f"수익률: {profit_rate:.2f}%")
            print("=" * 50)
                