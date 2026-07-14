def select_buy_trade(per_trade_results):

    print("\n[매도할 매수 거래 선택]")

    for result in per_trade_results:
        print(
            f"거래 ID: {result['id']} | "
            f"매수가: {result['price']:,.0f}원 | "
            f"보유수량: {result['quantity']:.8f}"
        )

    selected_trade_id = int(
        input("\n매도할 거래 ID를 입력하세요: ")
    )

    for result in per_trade_results:
        if result["id"] == selected_trade_id:
            return result

    return None