def calculate_asset(rows, current_price, fee_rate):

    # 총 보유수량
    total_quantity = 0

    # 총 매수금액
    total_buy_amount = 0

    for row in rows:

        # 1. 원본 데이터 꺼내기
        coin = row[1]
        price = row[4]
        quantity = row[5]

        # 2. 개별 거래 계산
        trade_amount = price * quantity
        fee_amount = trade_amount * fee_rate
        settlement_amount = trade_amount + fee_amount

        #3. 검산 출력
        print(f"price: {price:,.0f}원")
        print(f"quantity: {quantity:,.8f}개")
        print(f"trade_amount: {trade_amount:,.0f}원")
        print(f"fee_amount: {fee_amount:,.3f}원")
        print(f"settlement_amount: {settlement_amount:,.0f}원")
        print("\n" + "=" * 50)
        
        """
        value = current_price * quantity
        transaction_profit_loss = value - trade_amount
        transaction_profit_rate = (transaction_profit_loss / trade_amount) * 100

        print("\n" + "=" * 50)
        print(f"{row[0]} 번째 코인")
        print(f"{price:,.0f}원")
        print(f"평가금액: {value:,.0f}원")
        print(f"평가손익: {transaction_profit_loss:,.0f}원")
        print(f"수익률: {transaction_profit_rate:,.0f}%")

        if current_price > price:
            print("이익 🟢")
        else:
            print("손해 🔴")

        print("=" * 50)
        """

        # 4. 전체 합계 누적
        total_quantity += quantity
        total_buy_amount += settlement_amount

    # 평균 매수가
    average_buy_price = total_buy_amount / total_quantity

    # 현재 평가금액
    current_value = total_quantity * current_price

    # 평가손익
    profit_loss = current_value - total_buy_amount

    # 수익률
    profit_rate = (profit_loss / total_buy_amount) * 100

    return (
        total_quantity,
        total_buy_amount,
        average_buy_price,
        current_value,
        profit_loss,
        profit_rate)

