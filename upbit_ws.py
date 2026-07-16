import websocket
import json
from decimal import Decimal
from calculator import (
    calculate_asset,
    calculate_sell,
    filter_trades_by_market,
)

# 현재가 출력 함수, 예상 결과 출력
from printer import print_realtime_asset, print_sell_preview

# 거래 ID 입력, 매도 예정 가격 입력
from sell_manager import select_buy_trade, input_sell_plan

def watch_current_price(rows, fee_rate):

    market = "KRW-XRP"

    market_rows = filter_trades_by_market(
        rows,
        market
    )

    # WebSocket 연결 객체 생성
    ws = websocket.WebSocket()

    # 업비트 서버 연결
    ws.connect("wss://api.upbit.com/websocket/v1")
    print("업비트 WebSocket 연결 완료")

    # 구독 요청
    ws.send('[{"ticket":"test"},{"type":"ticker","codes":["KRW-XRP"]}]')
    print("구독 요청 완료")

    # 이전 가격 (현재 가격과 비교 위해)
    previous_price = None
    trade_selected = False

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
            ) = calculate_asset(market_rows, current_price, fee_rate)
            
            previous_price = current_price
            
            # 매도할 매수 거래 선택
            if not trade_selected:
                selected_trade = select_buy_trade(per_trade_results)

                if selected_trade is None:
                    print("존재하지 않는 거래 ID입니다.")

                else:
                    print("\n[선택한 거래]")
                    print(f"거래 ID: {selected_trade['id']}")
                    print(f"매수가: {selected_trade['price']:,.0f}원")
                    print(f"보유수량: {selected_trade['quantity']:.8f}")

                    sell_price, sell_quantity = input_sell_plan(
                        selected_trade
                    )

                    print("\n[매도 예정 정보]")
                    print(f"매도 예정가: {sell_price:,.0f}원")
                    print(f"매도 예정수량: {sell_quantity:.8f}")

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

                    # 예상 매도 출력
                    print_sell_preview(
                        selected_trade,
                        sell_price,
                        sell_quantity,
                        sell_fee_amount,
                        sell_settlement_amount,
                        realized_profit_loss,
                        realized_profit_rate,
                        remaining_quantity
                    )


                trade_selected = True

            # 현재가 출력 함수
            print_realtime_asset(
                current_price,
                total_quantity,
                total_buy_amount,
                average_buy_price,
                current_value,
                profit_loss,
                profit_rate,
                per_trade_results
            )
                
