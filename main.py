from database import get_trades
from calculator import calculate_asset, calculate_sell, calculate_trade_quantities
from decimal import Decimal # decimal으로 만들기
from upbit_ws import watch_current_price

# 출력
from printer import print_per_trade_results, print_current_price, print_asset_summary, print_sell_trade_results

# 거래내역 데이터 저장
rows = get_trades()

coin_totals = calculate_trade_quantities(rows)
# print(coin_totals)

"""
for market, totals in coin_totals.items():
    print(
        market,
        "매수:", totals["buy_quantity"],
        "매도:", totals["sell_quantity"],
    )
"""

# 수수료율
fee_rate = Decimal("0.0005") # fee_rate = 0.0005는 float 타입이라 

# 현재가
current_price = watch_current_price(rows, fee_rate)

# 매도 수량 및 매도 가격
sell_quantity = Decimal("237.86869647")
sell_price = Decimal("2102.0")

(total_quantity,
 total_buy_amount,
 average_buy_price,
 current_value,
 profit_loss,
 profit_rate,
 per_trade_results,
 sell_trade_results
 ) = calculate_asset(rows, current_price, fee_rate)

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

# 개별 거래 내역
print_per_trade_results(per_trade_results)

# 현재가 출력
print_current_price(current_price)

# 보유자산 출력
print_asset_summary(
    total_quantity,
    total_buy_amount,
    average_buy_price,
    current_value,
    profit_loss,
    profit_rate
)

# 매도 출력
print_sell_trade_results(sell_trade_results)