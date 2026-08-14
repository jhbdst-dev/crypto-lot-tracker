from decimal import Decimal

# 코인 1개의 자산 정보를 계산하는 함수
def calculate_coin_asset(
    market: str,                # 코인 이름
    quantity: Decimal,          # 현재 보유 수량
    average_buy_price: Decimal, # 평균 매수가
    current_price: Decimal,     # 현재가
):
    # 총 매수금액 = 보유수량 * 평균 매수가
    total_buy_amount = quantity * average_buy_price

    # 평가금액 = 보유수량 * 현재가
    evaluation_amount = quantity * current_price

    # 평가 손익 = 평가금액 - 총 매수금액
    evaluation_profit = evaluation_amount - total_buy_amount

    # 수익률 계산
    if total_buy_amount == 0:
        profit_rate = Decimal("0")
    else:
        # 수익률 = (평가 손익 / 총 매수금액) * 100
        profit_rate = (
            evaluation_profit / total_buy_amount
        ) * Decimal("100")

    return {
        "market": market,                       # 코인 이름
        "quantity": quantity,                   # 보유 수량
        "average_buy_price": average_buy_price, # 평균 매수가
        "current_price": current_price,         # 현재가
        "total_buy_amount": total_buy_amount,   # 총 매수금액
        "evaluation_amount": evaluation_amount, # 평가금액
        "evaluation_profit": evaluation_profit, # 평가 손익
        "profit_rate": profit_rate,             # 수익률
    }

# 홈 화면에 필요한 전체 자산 정보를 계산하는 함수
def calculate_home_summary(coin_results: list[dict]):

    # 전체 총 매수금액
    total_buy_amount = Decimal("0")

    # 전체 총 평가금액
    total_evaluation_amount = Decimal("0")

    # 코인별 계산 결과를 하나씩 합산
    for result in coin_results:
        total_buy_amount += result["total_buy_amount"]
        total_evaluation_amount += result["evaluation_amount"]

    # 전체 평가손익 = 전체 평가금액 - 전체 총 매수금액
    total_evaluation_profit = (
        total_evaluation_amount - total_buy_amount
    )

    # 전체 수익률
    if total_buy_amount == 0:
        total_profit_rate = Decimal("0")
    else:
        # 전체 수익률 = (전체 손익 / 전체 매수금액) * 100
        total_profit_rate = (
            total_evaluation_profit / total_buy_amount
        ) * Decimal("100")

    return {
        "total_buy_amount": total_buy_amount,               # 전체 총 매수금액
        "total_evaluation_amount": total_evaluation_amount, # 전체 평가금액
        "total_evaluation_profit": total_evaluation_profit, # 전체 평가손익
        "total_profit_rate": total_profit_rate,             # 전체 수익률
        "coin_count": len(coin_results),                    # 현재 보유한 코인의 개수
    }

# 전체 거래내역에서 특정 시장의 거래만 추출
def get_trades_by_market(rows, market):

    # 특정 시장의 거래내역 저장
    market_rows = []

    # 전체 거래내역을 한 행씩 확인
    for row in rows:

        # 요청한 시장과 일치하는 거래만 저장
        if row[2] == market:
            market_rows.append(row)

    # 특정 시장의 거래내역 반환
    return market_rows

# 현재 보유수량을 이루고 있는 매수 거래들을 찾는 함수
def get_current_buy_lots(rows, current_quantity):

    # 매수 거래만 추출
    buy_rows = [
        row
        for row in rows
        if row[3] == "bid"
    ]

    # 매수 거래를 최신순으로 정렬
    buy_rows.sort(
        key=lambda row: row[12],
        reverse=True,
    )

    # 최종적으로 남아있는 거래들을 저장할 리스트
    selected_lots = []

    # 아직 찾아야 하는 수량
    remaining_target = current_quantity

    # 최신 매수 거래부터 하나씩 확인
    for row in buy_rows:
        executed_volume = row[8]

        # 이미 필요한 수량을 다 찾았는지 확인
        if remaining_target <= 0:
            break

        # 해당 거래 전체가 남아 있는 경우
        if executed_volume <= remaining_target:
            remaining_quantity = executed_volume

        # 해당 거래의 일부만 남아 있는 경우
        else:
            remaining_quantity = remaining_target

        # 남아있는 거래 정보를 저장
        selected_lots.append({
            "row": row,
            "remaining_quantity": remaining_quantity,
        })

        # 찾아야 하는 수량 감소
        remaining_target -= remaining_quantity

    # 화면에서는 오래된 순서부터 표시
    selected_lots.sort(
        key=lambda lot: lot["row"][12]
    )

    return selected_lots