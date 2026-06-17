from database import get_trades
from calculator import calculate_asset

# 거래내역 데이터 저장
rows = get_trades()

# 외부 기준값 묶음

# 현재가
current_price = 1800

# 수수료율
fee_rate = 0.0005

(total_quantity,
 total_buy_amount,
 average_buy_price,
 current_value,
 profit_loss,
 profit_rate) = calculate_asset(rows, current_price, fee_rate)


print("\n" + "=" * 50)
print("             현재가")
print("=" * 50)

# 현재가
print(f"현재가: {current_price}")

print("\n" + "=" * 50)
print("             보유자산 화면")
print("=" * 50)

print(f"총 보유수량: {total_quantity:.8f}")
print(f"총 매수금액: {total_buy_amount:,.0f}원")
print(f"평균 매수가: {average_buy_price:,.2f}원")
print(f"현재 평가금액: {current_value:,.0f}원")
print(f"평가손익: {profit_loss:,.0f}원")
print(f"수익률: {profit_rate:.2f}%")

print("=" * 50)