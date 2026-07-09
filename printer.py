# 개별 거래 내역
def print_per_trade_results(per_trade_results):

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

# 현재가 출력
def print_current_price(current_price):
    print("\n" + "=" * 50)
    print("             현재가")
    print("=" * 50)
    print(f"현재가: {current_price}")

# 보유자산 출력
def print_asset_summary(
    total_quantity,
    total_buy_amount,
    average_buy_price,
    current_value,
    profit_loss,
    profit_rate
):
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

# 매도 출력
def print_sell_trade_results(sell_trade_results):
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