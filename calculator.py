def calculate_buy(row, current_price, fee_rate):

    # 1. 원본 데이터 꺼내기
    trade_type = row[3]
    price = row[4]
    quantity = row[5]

    # 2. 개별 거래 계산
    trade_amount = price * quantity
    fee_amount = trade_amount * fee_rate
    settlement_amount = trade_amount + fee_amount
    value = current_price * quantity
    transaction_profit_loss = value - settlement_amount
    transaction_profit_rate = (transaction_profit_loss / settlement_amount) * 100


    return {
    "id": row[0],
    "trade_type": trade_type,
    "price": price,
    "quantity": quantity,
    "trade_amount": trade_amount,
    "fee_amount": fee_amount,
    "settlement_amount": settlement_amount,
    "value": value,
    "profit_loss": transaction_profit_loss,
    "profit_rate": transaction_profit_rate
    }

def calculate_asset(rows, current_price, fee_rate):

    # 총 보유수량
    total_quantity = 0

    # 총 매수금액
    total_buy_amount = 0

    # 거래별 결과 저장 리스트
    per_trade_results = []

    # 매도 결과 저장 리스트
    sell_trade_results = []

    for row in rows:

        trade_type = row[3]

        if trade_type == "BUY":
            buy_result = calculate_buy(row, current_price, fee_rate)
            
            # 3. 전체 합계 누적
            total_quantity += buy_result["quantity"]
            total_buy_amount += buy_result["settlement_amount"]

            # 4. 출력
            per_trade_results.append(buy_result)

        elif trade_type == "SELL":
            sell_trade_results.append({
                "id": row[0],
                "trade_type": trade_type,
                "price": row[4],
                "quantity": row[5],
                "fee_amount": row[6],
                "settlement_amount": row[7],
                "trade_amount": row[9],
            })

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
        profit_rate,
        per_trade_results,
        sell_trade_results
        )

def calculate_sell(
        selected_trade,
        sell_quantity,
        sell_price,
        fee_rate
        ):
    
    # 선택한 거래 데이터
    selected_quantity = selected_trade["quantity"]
    selected_settlement_amount = selected_trade["settlement_amount"]
    
    # 선택한 거래의 1개당 실제 매수원가
    selected_buy_unit_cost = (
        selected_settlement_amount
        / selected_quantity
    )

    print(
        "1개당 실제 매수원가:",
        selected_buy_unit_cost
    )

    # 매도 거래금액
    sell_trade_amount = (
        sell_quantity
        * sell_price
    )

    # 남은 보유수량
    remaining_quantity = (
        selected_quantity
        - sell_quantity
    )

    # 매도 수수료
    sell_fee_amount = (
        sell_trade_amount
        * fee_rate
    )

    # 매도 정산금액
    sell_settlement_amount = (
    sell_trade_amount
    - sell_fee_amount
    )

    # 매도한 원가
    sold_buy_amount = (
    selected_buy_unit_cost
    * sell_quantity
    )

    # 실현손익
    realized_profit_loss = (
        sell_settlement_amount
        - sold_buy_amount
    )

    # 실현수익률
    realized_profit_rate = (
        realized_profit_loss
        / sold_buy_amount
    ) * 100

    # 남은 총 매수금액
    remaining_buy_amount = (
        selected_settlement_amount
        - sold_buy_amount
    )

    # 남은 평균 매수가
    remaining_average_buy_price = (
        remaining_buy_amount
        / remaining_quantity
    )

    return (
        sell_trade_amount,
        remaining_quantity,
        sell_fee_amount,
        sell_settlement_amount,
        sold_buy_amount,
        realized_profit_loss,
        realized_profit_rate,
        remaining_buy_amount,
        remaining_average_buy_price
    )
    