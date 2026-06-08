from database import get_trades
from calculator import calculate_asset

rows = get_trades()

total_quantity, total_buy_amount, average_buy_price = calculate_asset(rows)

print(f"총 보유수량: {total_quantity}")
print(f"총 매수금액: {total_buy_amount}")
print(f"평균 매수가: {average_buy_price}")