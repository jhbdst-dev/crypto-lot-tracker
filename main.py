from database import get_trades
from calculator import calculate_asset

# 거래내역 데이터 저장
rows = get_trades()

# 외부 기준값 묶음
current_prcie = 1770

(total_quantity,
 total_buy_amount,
 average_buy_price,
 current_value) = calculate_asset(rows, current_prcie)

print(f"총 보유수량: {total_quantity}")
print(f"총 매수금액: {total_buy_amount}")
print(f"평균 매수가: {average_buy_price}")
print(f"현재 평가금액: {current_value}")