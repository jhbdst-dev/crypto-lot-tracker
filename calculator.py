def calculate_asset(rows, current_price):

    # 총 보유수량
    total_quantity = 0

    # 총 매수금액
    total_buy_amount = 0

    for row in rows:

        # 필요한 데이터만 꺼내기
        coin = row[1]
        price = row[4]
        quantity = row[5]
        trade_amount = row[9]
        value = current_price * quantity

        print(f"{row[0]} 번째 코인")
        print(f"{price:,.0f}원")
        print(f"평가금액: {value:,.0f}원")

        if current_price > price:
            print("이익 🟢")
        else:
            print("손해 🔴")

        total_quantity += row[5]
        total_buy_amount += row[7]

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

