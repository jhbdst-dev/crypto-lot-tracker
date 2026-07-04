import websocket
import json
from decimal import Decimal

def get_current_price():
    # WebSocket 연결 객체 생성
    ws = websocket.WebSocket()

    # 업비트 서버 연결
    ws.connect("wss://api.upbit.com/websocket/v1")

    # 구독 요청
    ws.send('[{"ticket":"test"},{"type":"ticker","codes":["KRW-XRP"]}]')

    previous_price = None

    while True:
        data = ws.recv()
        data = json.loads(data)

        current_price = Decimal(str(data["trade_price"]))

        if current_price != previous_price:
            print(current_price)
            previous_price = current_price
    
    return current_price