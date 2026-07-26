from decimal import Decimal

# DB에서 조회한 거래 행(row)을 이름이 있는 딕셔너리로 변환
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

# 코인별 총 매수수량과 총 매도수량 계산
def calculate_trade_quantities(rows):
    
    # 코인별 매수·매도 수량 저장
    coin_totals = {}

    # 전체 거래내역을 한 행씩 확인
    for row in rows:

        # 현재 거래의 시장, 거래 방향, 체결수량 추출
        market = row[2]
        side = row[3]
        quantity = row[8]

        # 처음 등장한 코인이면 매수·매도 수량 저장 공간 생성
        if market not in coin_totals:
            coin_totals[market] = {
                "buy_quantity": 0,
                "sell_quantity": 0,
            }

        # 매수 거래이면 매수수량 누적
        if side == "bid":
            coin_totals[market]["buy_quantity"] += quantity

        # 매도 거래이면 매도수량 누적
        elif side == "ask":
            coin_totals[market]["sell_quantity"] += quantity

    # 코인별 총 매수·매도 수량 반환
    return coin_totals

# 코인별 현재 보유수량 계산
def calculate_current_holdings(coin_totals):

    # 현재 보유 중인 코인과 수량 저장
    current_holdings = {}

    # 코인별 총 매수·매도 수량 확인
    for market, totals in coin_totals.items():

        # 총 매수수량과 총 매도수량 추출
        buy_quantity = totals["buy_quantity"]
        sell_quantity = totals["sell_quantity"]

        # 현재 보유수량 계산
        holding_quantity = buy_quantity - sell_quantity

        # 보유수량이 남아 있는 코인만 저장
        if holding_quantity > 0:
            current_holdings[market] = holding_quantity

    # 현재 보유 중인 코인별 수량 반환
    return current_holdings

# 개별 매수 거래의 현재 평가금액과 손익 계산
def calculate_buy(row, current_price, fee_rate):

    # 거래 종류 설정
    trade_type = "BUY"

    # 매수 거래 정보 추출
    quantity = row[8]
    trade_amount = row[9]
    fee_amount = row[10]

    # 시장가 주문은 row[6]의 가격이 없을 수 있으므로
    # 실제 체결금액 ÷ 체결수량으로 매수가 계산
    price = trade_amount / quantity

    # 수수료를 포함한 실제 매수원가 계산
    settlement_amount = trade_amount + fee_amount

    # 현재가 기준 평가금액 계산
    value = current_price * quantity

    # 개별 매수 거래의 평가손익 계산
    transaction_profit_loss = (
        value - settlement_amount
    )

    # 개별 매수 거래의 수익률 계산
    transaction_profit_rate = (
        transaction_profit_loss
        / settlement_amount
    ) * 100

    # 개별 매수 거래 계산 결과 반환
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

# 전체 보유자산과 개별 거래 손익 계산
def calculate_asset(rows, current_price, fee_rate):

    # 총 보유수량
    total_quantity = 0

    # 총 매수금액
    total_buy_amount = 0

    # 개별 매수 거래 계산 결과 저장
    per_trade_results = []

    # 실제 매도 거래내역 저장
    sell_trade_results = []

    # 전체 거래내역을 한 행씩 확인
    for row in rows:

        # 매수 거래만 개별 계산
        if row[3] == "bid":

            buy_result = calculate_buy(
                row,
                current_price,
                fee_rate
            )

            # 전체 매수수량과 총 매수원금 누적
            total_quantity += buy_result["quantity"]
            total_buy_amount += buy_result["settlement_amount"]

            # 개별 매수 거래 결과 저장
            per_trade_results.append(buy_result)

    # 현재 남아 있는 매수 거래가 없으면 계산 중단
    if total_quantity == 0:
        raise ValueError(
            "매수 거래가 없어 자산을 계산할 수 없습니다."
        )

    # 평균 매수가 계산
    average_buy_price = total_buy_amount / total_quantity

    # 현재 평가금액 계산
    current_value = total_quantity * current_price

    # 전체 평가손익 계산
    profit_loss = current_value - total_buy_amount

    # 전체 수익률 계산
    profit_rate = (profit_loss / total_buy_amount) * 100

    # 전체 자산과 개별 거래 결과 반환
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

# 선택한 매수 거래의 예상 매도 결과 계산
def calculate_sell(
        selected_trade,
        sell_quantity,
        sell_price,
        fee_rate
        ):
    
    # 선택한 매수 거래 정보 추출
    selected_quantity = selected_trade["quantity"]
    selected_settlement_amount = selected_trade["settlement_amount"]
    
    # 선택한 거래의 1개당 실제 매수원가 계산
    selected_buy_unit_cost = (
        selected_settlement_amount
        / selected_quantity
    )

    # 예상 매도 거래금액 계산
    sell_trade_amount = (
        sell_quantity
        * sell_price
    )

    # 매도 후 남은 보유수량 계산
    remaining_quantity = (
        selected_quantity
        - sell_quantity
    )

    # 예상 매도 수수료 계산
    sell_fee_amount = (
        sell_trade_amount
        * fee_rate
    )

    # 수수료 차감 후 예상 매도 정산금액 계산
    sell_settlement_amount = (
    sell_trade_amount
    - sell_fee_amount
    )

    # 매도한 수량에 해당하는 기존 매수원가 계산
    sold_buy_amount = (
    selected_buy_unit_cost
    * sell_quantity
    )

    # 예상 실현손익 계산
    realized_profit_loss = (
        sell_settlement_amount
        - sold_buy_amount
    )

    # 예상 실현수익률 계산
    realized_profit_rate = (
        realized_profit_loss
        / sold_buy_amount
    ) * 100

    # 매도 후 남은 총 매수금액 계산
    remaining_buy_amount = (
        selected_settlement_amount
        - sold_buy_amount
    )

    # 매도 후 남은 평균 매수가 계산
    if remaining_quantity == 0:
        remaining_average_buy_price = Decimal("0")
    else:
        remaining_average_buy_price = (
            remaining_buy_amount
            / remaining_quantity
        )

    # 예상 매도 결과 반환
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
    
# 전체 거래내역에서 특정 시장의 거래만 추출
def filter_trades_by_market(rows, market):

    # 특정 시장의 거래내역 저장
    market_rows = []

    # 전체 거래내역을 한 행씩 확인
    for row in rows:

        # 요청한 시장과 일치하는 거래만 저장
        if row[2] == market:
            market_rows.append(row)

    # 특정 시장의 거래내역 반환
    return market_rows