import websocket
import json
from decimal import Decimal

# 자산·매도 계산 및 시장별 거래 필터링
from backend.calculator import (
    calculate_asset,
    calculate_sell,
    filter_trades_by_market,
)

# 매도할 거래 선택 및 매도 조건 입력
from backend.sell_manager import (
    select_buy_trade,
    input_sell_plan
    )

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
    previous_price = None

    # 매도할 거래를 이미 선택했는지 확인
    trade_selected = False

    # WebSocket 데이터를 계속 수신
    while True:

        # 실시간 데이터 수신
        data = ws.recv()

        # JSON 문자열을 파이썬 딕셔너리로 변환
        data = json.loads(data)

        # 현재 수신한 코인의 시장 코드 추출
        market = data["code"]

        # 현재는 BTC 데이터만 처리
        if market != "KRW-BTC":
            continue
        
        # 실시간 체결가격을 Decimal 타입으로 변환
        current_price = Decimal(str(data["trade_price"]))

        # 전체 거래내역에서 현재 코인의 거래만 추출
        market_rows = filter_trades_by_market(
            rows,
            market
        )

        # 현재가가 이전 가격과 달라졌을 때만 다시 계산
        if current_price != previous_price:
            
            # 현재 코인의 보유자산과 개별 거래 손익 계산
            (
                total_quantity,
                total_buy_amount,
                average_buy_price,
                current_value,
                profit_loss,
                profit_rate,
                per_trade_results,
                sell_trade_results
            ) = calculate_asset(market_rows, current_price, fee_rate)
            
            # 현재가를 다음 비교를 위한 이전 가격으로 저장
            previous_price = current_price
            
            # 프로그램 실행 후 한 번만 매도 거래 선택
            if not trade_selected:

                # 매도할 매수 거래 선택
                selected_trade = select_buy_trade(per_trade_results)

                # 거래를 선택하지 못한 경우
                if selected_trade is None:
                    print("존재하지 않는 거래 ID입니다.")

                # 거래를 정상적으로 선택한 경우
                else:
                    
                    # 선택한 매수 거래 정보 출력
                    print("\n[선택한 거래]")
                    print(f"거래 ID: {selected_trade['id']}")
                    print(f"매수가: {selected_trade['price']:,.0f}원")
                    print(f"보유수량: {selected_trade['quantity']:.8f}")

                    # 예상 매도 가격과 수량 입력
                    sell_price, sell_quantity = input_sell_plan(
                        selected_trade
                    )

                    # 입력한 예상 매도 조건 출력
                    print("\n[매도 예정 정보]")
                    print(f"매도 예정가: {sell_price:,.0f}원")
                    print(f"매도 예정수량: {sell_quantity:.8f}")

                    # 선택한 거래의 예상 매도 결과 계산
                    (
                        sell_trade_amount,
                        remaining_quantity,
                        sell_fee_amount,
                        sell_settlement_amount,
                        sold_buy_amount,
                        realized_profit_loss,
                        realized_profit_rate,
                        remaining_buy_amount,
                        remaining_average_buy_price
                    ) = calculate_sell(
                        selected_trade,
                        sell_quantity,
                        sell_price,
                        fee_rate
                    )

                # 매도 거래 선택 과정을 다시 실행하지 않도록 설정
                trade_selected = True


