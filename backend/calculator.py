from decimal import Decimal

def parse_trade_row(row):
    return {
        "id": row[0],
        "uuid": row[1],
        "market": row[2],
        "side": row[3],
        "ord_type": row[4],
        "state": row[5],
        "price": row[6],
        "volume": row[7],
        "executed_volume": row[8],
        "executed_funds": row[9],
        "paid_fee": row[10],
        "trades_count": row[11],
        "created_at": row[12],
    }

def calculate_trade_quantities(rows):
    coin_totals = {}

    for row in rows:
        market = row[2]
        side = row[3]
        quantity = row[8]

        if market not in coin_totals:
            coin_totals[market] = {
                "buy_quantity": 0,
                "sell_quantity": 0,
            }

        if side == "bid":
            coin_totals[market]["buy_quantity"] += quantity

        elif side == "ask":
            coin_totals[market]["sell_quantity"] += quantity

    return coin_totals

def calculate_current_holdings(coin_totals):
    current_holdings = {}

    for market, totals in coin_totals.items():
        buy_quantity = totals["buy_quantity"]
        sell_quantity = totals["sell_quantity"]

        holding_quantity = buy_quantity - sell_quantity

        if holding_quantity > 0:
            current_holdings[market] = holding_quantity

    return current_holdings

def calculate_buy(row, current_price, fee_rate):

    trade_type = "BUY"

    quantity = row[8]
    trade_amount = row[9]
    fee_amount = row[10]

    # 시장가 주문은 row[6]의 가격이 없을 수 있으므로
    # 실제 체결금액 ÷ 체결수량으로 매수가 계산
    price = trade_amount / quantity

    settlement_amount = trade_amount + fee_amount
    value = current_price * quantity

    transaction_profit_loss = (
        value - settlement_amount
    )

    transaction_profit_rate = (
        transaction_profit_loss
        / settlement_amount
    ) * 100

    return {
        "id": row[0],
        "market": row[2],
        "trade_type": trade_type,
        "price": price,
        "quantity": quantity,
        "trade_amount": trade_amount,
        "fee_amount": fee_amount,
        "settlement_amount": settlement_amount,
        "value": value,
        "profit_loss": transaction_profit_loss,
        "profit_rate": transaction_profit_rate,
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

    remaining_buy_lots = calculate_remaining_buy_lots(rows)

    for lot in remaining_buy_lots:
        row = lot["row"]
        remaining_quantity = lot["remaining_quantity"]

        buy_result = calculate_buy(
            row,
            current_price,
            fee_rate
        )

        # 원래 매수수량 대신 매도 후 남은 수량 적용
        original_quantity = buy_result["quantity"]

        quantity_ratio = (
            remaining_quantity
            / original_quantity
        )

        buy_result["quantity"] = remaining_quantity
        buy_result["trade_amount"] *= quantity_ratio
        buy_result["fee_amount"] *= quantity_ratio
        buy_result["settlement_amount"] *= quantity_ratio
        buy_result["value"] = (
            current_price
            * remaining_quantity
        )
        buy_result["profit_loss"] = (
            buy_result["value"]
            - buy_result["settlement_amount"]
        )
        buy_result["profit_rate"] = (
            buy_result["profit_loss"]
            / buy_result["settlement_amount"]
        ) * 100

        total_quantity += buy_result["quantity"]
        total_buy_amount += buy_result["settlement_amount"]

        per_trade_results.append(buy_result)

    # 실제 매도 거래내역 저장
    for row in rows:
        if row[3] == "ask":
            sell_trade_results.append({
                "id": row[0],
                "market": row[2],
                "trade_type": "SELL",
                "price": row[9] / row[8],
                "quantity": row[8],
                "trade_amount": row[9],
                "fee_amount": row[10],
                "settlement_amount": row[9] - row[10],
            })

    if total_quantity == 0:
        raise ValueError(
            "매수 거래가 없어 자산을 계산할 수 없습니다."
        )

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
    if remaining_quantity == 0:
        remaining_average_buy_price = Decimal("0")
    else:
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
    
def filter_trades_by_market(rows, market):
    market_rows = []

    for row in rows:
        if row[2] == market:
            market_rows.append(row)

    return market_rows

def calculate_remaining_buy_lots(rows):
    # 거래를 오래된 순서대로 정렬
    sorted_rows = sorted(
        rows,
        key=lambda row: row[12]
    )

    buy_lots = []

    for row in sorted_rows:
        side = row[3]
        quantity = row[8]

        # 매수 거래 저장
        if side == "bid":
            buy_lots.append({
                "row": row,
                "remaining_quantity": quantity,
            })

        # 매도 수량을 오래된 매수 거래부터 차감
        elif side == "ask":
            sell_quantity = quantity

            for lot in buy_lots:
                if sell_quantity <= 0:
                    break

                remaining_quantity = lot["remaining_quantity"]

                if remaining_quantity <= sell_quantity:
                    sell_quantity -= remaining_quantity
                    lot["remaining_quantity"] = Decimal("0")

                else:
                    lot["remaining_quantity"] -= sell_quantity
                    sell_quantity = Decimal("0")

    # 수량이 남아 있는 매수 거래만 반환
    return [
        lot
        for lot in buy_lots
        if lot["remaining_quantity"] > 0
    ]