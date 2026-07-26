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