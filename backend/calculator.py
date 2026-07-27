from decimal import Decimal


def calculate_coin_asset(
    market: str,
    quantity: Decimal,
    average_buy_price: Decimal,
    current_price: Decimal,
):
    total_buy_amount = quantity * average_buy_price
    evaluation_amount = quantity * current_price
    evaluation_profit = evaluation_amount - total_buy_amount

    if total_buy_amount == 0:
        profit_rate = Decimal("0")
    else:
        profit_rate = (
            evaluation_profit / total_buy_amount
        ) * Decimal("100")

    return {
        "market": market,
        "quantity": quantity,
        "average_buy_price": average_buy_price,
        "current_price": current_price,
        "total_buy_amount": total_buy_amount,
        "evaluation_amount": evaluation_amount,
        "evaluation_profit": evaluation_profit,
        "profit_rate": profit_rate,
    }

def calculate_home_summary(coin_results: list[dict]):
    # 전체 총 매수금액
    total_buy_amount = Decimal("0")

    # 전체 총 평가금액
    total_evaluation_amount = Decimal("0")

    # 코인별 계산 결과를 하나씩 합산
    for result in coin_results:
        total_buy_amount += result["total_buy_amount"]
        total_evaluation_amount += result["evaluation_amount"]

    # 전체 평가손익
    total_evaluation_profit = (
        total_evaluation_amount - total_buy_amount
    )

    # 전체 수익률
    if total_buy_amount == 0:
        total_profit_rate = Decimal("0")
    else:
        total_profit_rate = (
            total_evaluation_profit / total_buy_amount
        ) * Decimal("100")

    return {
        "total_buy_amount": total_buy_amount,
        "total_evaluation_amount": total_evaluation_amount,
        "total_evaluation_profit": total_evaluation_profit,
        "total_profit_rate": total_profit_rate,
        "coin_count": len(coin_results),
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

def get_current_buy_cycle(rows):
    # 오래된 거래부터 계산
    sorted_rows = sorted(
        rows,
        key=lambda row: row[12],
    )

    current_quantity = Decimal("0")
    current_buy_rows = []

    for row in sorted_rows:
        side = row[3]
        executed_volume = row[8]

        # 매수
        if side == "bid":
            current_quantity += executed_volume
            current_buy_rows.append(row)

        # 매도
        elif side == "ask":
            current_quantity -= executed_volume

            # 보유수량이 모두 정리되면
            # 이전 매수 사이클은 끝난 것
            if current_quantity <= 0:
                current_quantity = Decimal("0")
                current_buy_rows = []

    return current_buy_rows

def get_current_buy_lots(rows, current_quantity):
    # 매수 거래만 최신순으로 정렬
    buy_rows = [
        row
        for row in rows
        if row[3] == "bid"
    ]

    buy_rows.sort(
        key=lambda row: row[12],
        reverse=True,
    )

    selected_lots = []
    remaining_target = current_quantity

    for row in buy_rows:
        executed_volume = row[8]

        if remaining_target <= 0:
            break

        # 해당 거래 전체가 남아 있는 경우
        if executed_volume <= remaining_target:
            remaining_quantity = executed_volume

        # 해당 거래의 일부만 남아 있는 경우
        else:
            remaining_quantity = remaining_target

        selected_lots.append({
            "row": row,
            "remaining_quantity": remaining_quantity,
        })

        remaining_target -= remaining_quantity

    # 화면에서는 오래된 순서부터 표시
    selected_lots.sort(
        key=lambda lot: lot["row"][12]
    )

    return selected_lots