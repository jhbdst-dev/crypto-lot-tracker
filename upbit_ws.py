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
        print("데이터 수신")

        data = json.loads(data)
        current_price = Decimal(str(data["trade_price"]))

        if current_price != previous_price:
            calculate_asset(rows, current_price, fee_rate)
            previous_price = current_price
    
        result = calculate_asset(rows, current_price, fee_rate)
        print(result)