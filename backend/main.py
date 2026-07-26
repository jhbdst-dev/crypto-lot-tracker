from backend.database import get_trades

# 계산


from decimal import Decimal # decimal으로 만들기
from backend.upbit_ws import watch_current_price
from backend.upbit_accounts import get_account_assets

# 출력
from backend.printer import print_calculated_assets

# DB 거래내역 조회
rows = get_trades()

# 업비트 계좌의 실제 보유자산 조회
assets = get_account_assets()

# 업비트 거래 수수료율 설정
fee_rate = Decimal("0.0005") # fee_rate = 0.0005는 float 타입이라 

# 코인별 계산 결과를 저장할 딕셔너리
calculated_assets = {}

print_calculated_assets(calculated_assets)

raise SystemExit

# 실시간 현재가 수신
current_price = watch_current_price(rows, fee_rate, assets)

# 전체 자산 및 개별 거래 손익 계산
(total_quantity,
 total_buy_amount,
 average_buy_price,
 current_value,
 profit_loss,
 profit_rate,
 per_trade_results,
 sell_trade_results
 ) = calculate_asset(
    rows, 
    current_price, 
    fee_rate
)

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
    fee_rate,
    average_buy_price
)

