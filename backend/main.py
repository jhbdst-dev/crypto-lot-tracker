from backend.database import get_trades
from backend.calculator import (
    calculate_asset,
    calculate_sell,
    calculate_trade_quantities,
    calculate_current_holdings,
    filter_trades_by_market
    )
from decimal import Decimal # decimal으로 만들기
from backend.upbit_ws import watch_current_price
from backend.upbit_accounts import get_account_assets

# 출력


# DB 거래내역 조회
rows = get_trades()

# 코인별 총 매수·매도 수량 계산
coin_totals = calculate_trade_quantities(rows)

# BTC 거래내역 필터링
btc_rows = filter_trades_by_market(rows, "KRW-BTC")





# 코인별 현재 보유수량 계산
current_holdings = calculate_current_holdings(coin_totals)



# 업비트 계좌의 실제 보유자산 조회
assets = get_account_assets()



# 업비트 거래 수수료율 설정
fee_rate = Decimal("0.0005") # fee_rate = 0.0005는 float 타입이라 

# 실시간 현재가 수신
current_price = watch_current_price(rows, fee_rate, assets)

# 예상 매도 조건 설정
sell_quantity = Decimal("237.86869647")
sell_price = Decimal("2102.0")

# 전체 자산 및 개별 거래 손익 계산
(total_quantity,
 total_buy_amount,
 average_buy_price,
 current_value,
 profit_loss,
 profit_rate,
 per_trade_results,
 sell_trade_results
 ) = calculate_asset(rows, current_price, fee_rate)

# 예상 매도 결과 계산
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
    total_quantity,
    total_buy_amount,
    sell_quantity,
    sell_price,
    fee_rate,
    average_buy_price
)

