from decimal import Decimal, InvalidOperation

def select_buy_trade(per_trade_results):

    print("\n[매도할 매수 거래 선택]")

    for result in per_trade_results:
        print(
            f"거래 ID: {result['id']} | "
            f"매수가: {result['price']:,.0f}원 | "
            f"보유수량: {result['quantity']:.8f}"
        )

    while True:
        try:
            selected_trade_id = int(
                input("\n매도할 거래 ID를 입력하세요: ")
            )

        except ValueError:
            print("거래 ID는 숫자로 입력해주세요.")
            continue

        for result in per_trade_results:
            if result["id"] == selected_trade_id:
                return result

        print("존재하지 않는 거래 ID입니다. 다시 입력해주세요.")

def input_sell_plan(selected_trade):
    while True:
        try:
            sell_price = Decimal(
                input("매도 예정 가격을 입력하세요: ")
            )

            if sell_price <= 0:
                print("매도 가격은 0보다 커야 합니다.")
                continue

            break

        except InvalidOperation:
            print("숫자로 입력해주세요.")

    while True:
        try:
            sell_quantity = Decimal(
                input("매도 예정 수량을 입력하세요: ")
            )

            if sell_quantity <= 0:
                print("매도 수량은 0보다 커야 합니다.")
                continue

            if sell_quantity > selected_trade["quantity"]:
                print("보유수량보다 많이 매도할 수 없습니다.")
                continue

            break

        except InvalidOperation:
            print("숫자로 입력해주세요.")

    return sell_price, sell_quantity