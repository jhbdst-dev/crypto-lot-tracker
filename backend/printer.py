def print_coin_asset(result):
    print(f"\n=== {result['market']} 보유 자산 ===")
    print(f"보유수량: {result['quantity']}")
    print(f"평균 매수가: {result['average_buy_price']:,.2f}원")
    print(f"현재가: {result['current_price']:,.2f}원")
    print(f"총 매수금액: {result['total_buy_amount']:,.2f}원")
    print(f"평가금액: {result['evaluation_amount']:,.2f}원")
    print(f"평가손익: {result['evaluation_profit']:,.2f}원")
    print(f"수익률: {result['profit_rate']:,.2f}%")