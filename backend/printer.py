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

# 예상 결과 출력
def print_sell_preview(
        selected_trade,
        sell_price,
        sell_quantity,
        sell_fee_amount,
        sell_settlement_amount,
        realized_profit_loss,
        realized_profit_rate,
        remaining_quantity
        ):

    if realized_profit_loss > 0:
        status = "🟢"
    elif realized_profit_loss < 0:
        status = "🔴"
    else:
        status = "⚪"

    print("\n" + "=" * 50)
    print("예상 매도 결과")
    print("=" * 50)

    print(f"{status} 선택 거래 ID: {selected_trade['id']}")
    print(f"선택한 매수가: {selected_trade['price']:,.0f}원")
    print(f"매도 예정가: {sell_price:,.0f}원")
    print(f"매도 예정수량: {sell_quantity:.8f}")
    print(f"예상 수수료: {sell_fee_amount:,.0f}원")
    print(f"예상 정산금액: {sell_settlement_amount:,.0f}원")
    print(f"예상 실현손익: {realized_profit_loss:,.0f}원")
    print(f"예상 실현수익률: {realized_profit_rate:.2f}%")
    print(f"매도 후 남은 수량: {remaining_quantity:.8f}")

    print("=" * 50)

# 코인별 보유자산 출력
def print_coin_asset(
    current_price,
    total_quantity,
    total_buy_amount,
    average_buy_price,
    current_value,
    profit_loss,
    profit_rate
):
    if profit_loss > 0:
        status = "🟢"
    elif profit_loss < 0:
        status = "🔴"
    else:
        status = "⚪"

    print("\n" + "=" * 50)
    print("코인별 보유자산")
    print("=" * 50)
    print(f"현재가: {current_price:,.0f}원")
    print(f"총 보유수량: {total_quantity:.8f}")
    print(f"총 매수금액: {total_buy_amount:,.0f}원")
    print(f"평균 매수가: {average_buy_price:,.2f}원")
    print(f"현재 평가금액: {current_value:,.0f}원")
    print(f"{status} 평가손익: {profit_loss:,.0f}원")
    print(f"{status} 수익률: {profit_rate:.2f}%")
    print("=" * 50)

# 개별 코인 매수 거래 출력
def print_buy_trades(
    current_price,
    per_trade_results
):
    print("\n[개별 매수 거래]")

    for result in per_trade_results:

        if result["profit_loss"] > 0:
            status = "🟢"
        elif result["profit_loss"] < 0:
            status = "🔴"
        else:
            status = "⚪"

        print(
            f"{status} 거래 ID: {result['id']} | "
            f"현재가: {current_price:,.0f}원 | "
            f"매수가: {result['price']:,.0f}원 | "
            f"수량: {result['quantity']:.8f} | "
            f"평가금액: {result['value']:,.0f}원 | "
            f"평가손익: {result['profit_loss']:,.0f}원 | "
            f"수익률: {result['profit_rate']:.2f}%"
        )

# 실시간 자산 전체 출력
def print_realtime_asset(
    current_price,
    total_quantity,
    total_buy_amount,
    average_buy_price,
    current_value,
    profit_loss,
    profit_rate,
    per_trade_results
):
    """
    print_coin_asset(
        current_price,
        total_quantity,
        total_buy_amount,
        average_buy_price,
        current_value,
        profit_loss,
        profit_rate
    )


    print_buy_trades(
        current_price,
        per_trade_results
    )
    """