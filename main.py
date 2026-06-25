from database import get_trades
from calculator import calculate_asset
from calculator import calculate_sell
from decimal import Decimal # decimal으로 만들기

# 거래내역 데이터 저장
rows = get_trades()

# 현재가
current_price = 1783

# 매도 수량 및 매도 가격
sell_quantity = Decimal("237.86869647")
sell_price = Decimal("2102.0")

# 수수료율
fee_rate = Decimal("0.0005") # fee_rate = 0.0005는 float 타입이라 

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

for trade in per_trade_results:
    print("\n" + "=" * 50)
    print(f"{trade['id']} 번째 코인")
    print(f"종류: {trade['trade_type']}")
    print(f"매수가: {trade['price']:,.0f}원")
    print(f"수량: {trade['quantity']:,.8f}개")
    print(f"거래금액: {trade['trade_amount']:,.0f}원")
    print(f"수수료: {trade['fee_amount']:,.3f}원")
    print(f"정산금액: {trade['settlement_amount']:,.0f}원")
    print(f"평가금액: {trade['value']:,.0f}원")
    print(f"평가손익: {trade['profit_loss']:,.0f}원")
    print(f"수익률: {trade['profit_rate']:,.2f}%")

    if trade['profit_loss'] > 0:
        print("이익 🟢")
    else:
        print("손해 🔴")


# 매도 결과
print("\n" + "=" * 50)
print("             매도 결과")
print("=" * 50)

for sell in sell_trade_results:
    print("\n" + "=" * 50)
    print(f"{sell['id']} 번째 매도 거래")
    print(f"종류: {sell['trade_type']}")
    print(f"매도가: {sell['price']:,.0f}원")
    print(f"수량: {sell['quantity']:,.8f}개")
    print(f"거래금액: {sell['trade_amount']:,.0f}원")
    print(f"수수료: {sell['fee_amount']:,.3f}원")
    print(f"정산금액: {sell['settlement_amount']:,.0f}원")

print("=" * 50)

# 현재가
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