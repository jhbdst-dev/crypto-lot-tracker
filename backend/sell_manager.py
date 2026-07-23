from decimal import Decimal, InvalidOperation

"""
sell_manager.py

사용자가 매도할 거래를 선택하고,
예상 매도 가격과 수량을 입력받는 파일
"""

# 매도할 매수 거래 선택
def select_buy_trade(per_trade_results):

    # 매도 가능한 매수 거래 목록 출력
    print("\n[매도할 매수 거래 선택]")

    # 개별 매수 거래 목록 출력
    for result in per_trade_results:
        print(
            f"거래 ID: {result['id']} | "
            f"매수가: {result['price']:,.0f}원 | "
            f"보유수량: {result['quantity']:.8f}"
        )

    # 올바른 거래 ID가 입력될 때까지 반복
    while True:
        
        # 거래 ID 입력
        try:
            selected_trade_id = int(
                input("\n매도할 거래 ID를 입력하세요: ")
            )

        # 숫자가 아니면 다시 입력
        except ValueError:
            print("거래 ID는 숫자로 입력해주세요.")
            continue

        # 입력한 거래 ID 찾기
        for result in per_trade_results:

            # 선택한 거래 반환
            if result["id"] == selected_trade_id:
                return result

        # 존재하지 않는 ID인 경우
        print("존재하지 않는 거래 ID입니다. 다시 입력해주세요.")

# 예상 매도 가격과 수량 입력
def input_sell_plan(selected_trade):

    # 올바른 매도 가격 입력
    while True:

        # 매도 예정 가격 입력
        try:
            sell_price = Decimal(
                input("매도 예정 가격을 입력하세요: ")
            )

            # 0 이하 입력 방지
            if sell_price <= 0:
                print("매도 가격은 0보다 커야 합니다.")
                continue

            break

        # 숫자가 아니면 다시 입력
        except InvalidOperation:
            print("숫자로 입력해주세요.")

     # 올바른 매도 수량 입력
    while True:

        # 매도 예정 수량 입력
        try:
            sell_quantity = Decimal(
                input("매도 예정 수량을 입력하세요: ")
            )

            # 0 이하 입력 방지
            if sell_quantity <= 0:
                print("매도 수량은 0보다 커야 합니다.")
                continue

            # 보유수량 초과 입력 방지
            if sell_quantity > selected_trade["quantity"]:
                print("보유수량보다 많이 매도할 수 없습니다.")
                continue

            break

        # 숫자가 아니면 다시 입력
        except InvalidOperation:
            print("숫자로 입력해주세요.")

    # 입력한 매도 계획 반환
    return sell_price, sell_quantity