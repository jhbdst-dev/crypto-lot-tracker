import websocket
import json
from decimal import Decimal

from backend.calculator import calculate_coin_asset
from backend.printer import print_coin_asset
from backend.upbit_accounts import get_account_assets


# 업비트 WebSocket에서 실시간 현재가를 수신하고 자산을 계산
def watch_current_price(rows, fee_rate, assets):

    # 실제 보유 중인 코인의 시장 코드 목록 생성
    markets = list(assets.keys())

    # WebSocket 연결 객체 생성
    ws = websocket.WebSocket()

    # 업비트 WebSocket 서버 연결
    ws.connect("wss://api.upbit.com/websocket/v1")
    print("업비트 WebSocket 연결 완료")

    # 실시간 현재가 구독 요청 데이터 생성
    subscribe_data = [
        {"ticket": "asset-tracker"},
        {
            "type": "ticker",
            "codes": markets,
        },
    ]

    # 구독 요청을 JSON으로 변환하여 서버에 전송
    ws.send(json.dumps(subscribe_data))
    print("구독 요청 완료")

    # 직전에 계산한 현재가 저장
    previous_prices = {}

    # WebSocket 데이터를 계속 수신
    while True:

        # 실시간 데이터 수신
        data = ws.recv()

        # JSON 문자열을 파이썬 딕셔너리로 변환
        data = json.loads(data)

        # 현재 수신한 코인의 시장 코드 추출
        market = data["code"]
        
        # 실시간 체결가격을 Decimal 타입으로 변환
        current_price = Decimal(str(data["trade_price"]))

        # 전체 거래내역에서 현재 코인의 거래만 추출
        previous_price = previous_prices.get(market)

        if current_price != previous_price:
            asset = assets[market]

            result = calculate_coin_asset(
                market=market,
                quantity=asset["quantity"],
                average_buy_price=asset["average_buy_price"],
                current_price=current_price,
            )

            print_coin_asset(result)

            previous_prices[market] = current_price

if __name__ == "__main__":
    assets = get_account_assets()

    watch_current_price(
        rows=[],
        fee_rate=Decimal("0.0005"),
        assets=assets,
    )