from fastapi import FastAPI, HTTPException

from backend.calculator import (
    calculate_coin_asset,
    calculate_home_summary,
    get_trades_by_market,
    get_current_buy_lots,
)

from backend.database import get_trades

from backend.upbit_accounts import get_account_assets
from backend.upbit_prices import get_current_prices

from fastapi.middleware.cors import CORSMiddleware

from decimal import Decimal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Hello FastAPI!",
    }


@app.get("/home")
def get_home():
    # 보유 코인, 보유수량, 평균 매수가 조회
    assets = get_account_assets()

    # 보유 코인들의 현재가 조회
    markets = list(assets.keys())
    current_prices = get_current_prices(markets)

    # 계산 결과 저장
    coin_results = []

    for market, asset in assets.items():
        result = calculate_coin_asset(
            market=market,
            quantity=asset["quantity"],
            average_buy_price=asset["average_buy_price"],
            current_price=current_prices[market],
        )

        coin_results.append(result)

        # 전체 자산 요약 계산
        summary = calculate_home_summary(coin_results)

        # Decimal은 JSON으로 바로 보내기 어려우므로 숫자로 변환
        coins = []


        for result in coin_results:
            coins.append({
                "market": result["market"],
                "quantity": float(result["quantity"]),
                "average_buy_price": float(result["average_buy_price"]),
                "current_price": float(result["current_price"]),
                "total_buy_amount": float(result["total_buy_amount"]),
                "evaluation_amount": float(result["evaluation_amount"]),
                "evaluation_profit": float(result["evaluation_profit"]),
                "profit_rate": float(result["profit_rate"]),
            })

    return {
        "summary": {
            "total_buy_amount": float(summary["total_buy_amount"]),
            "total_evaluation_amount": float(
                summary["total_evaluation_amount"]
            ),
            "total_evaluation_profit": float(
                summary["total_evaluation_profit"]
            ),
            "total_profit_rate": float(
                summary["total_profit_rate"]
            ),
            "coin_count": summary["coin_count"],
        },
        "coins": coins,
    }

COIN_NAMES = {
    "KRW-BTC": "비트코인",
    "KRW-ETH": "이더리움",
    "KRW-XRP": "리플",
}

@app.get("/coins/{market}")
def get_coin_detail(market: str):
    market = market.upper()

    if market not in COIN_NAMES:
        raise HTTPException(
            status_code=404,
            detail=f"지원하지 않는 마켓입니다: {market}",
        )

    # 업비트 계좌에서 실제 보유자산 조회
    assets = get_account_assets()

    if market not in assets:
        raise HTTPException(
            status_code=404,
            detail=f"보유 중인 코인이 아닙니다: {market}",
        )

    # 요청받은 코인 하나의 현재가 조회
    current_prices = get_current_prices([market])
    current_price = current_prices[market]

    # 요청받은 코인의 계좌 정보
    asset = assets[market]

    # 홈 화면과 같은 계산 함수 사용
    result = calculate_coin_asset(
        market=market,
        quantity=asset["quantity"],
        average_buy_price=asset["average_buy_price"],
        current_price=current_price,
    )

    rows = get_trades()
    market_rows = get_trades_by_market(rows, market)
    current_buy_lots = get_current_buy_lots(
        market_rows,
        asset["quantity"],
    )

    buy_trades = []

    for lot in current_buy_lots:
        row = lot["row"]
        remaining_quantity = lot["remaining_quantity"]

        executed_volume = row[8]
        executed_funds = row[9]
        paid_fee = row[10]

        buy_price = executed_funds / executed_volume

        # 원래 거래 중 남은 비율
        remaining_ratio = (
            remaining_quantity / executed_volume
        )

        remaining_buy_amount = (
            executed_funds * remaining_ratio
        )

        remaining_fee_amount = (
            paid_fee * remaining_ratio
        )

        evaluation_amount = (
            remaining_quantity * current_price
        )

        evaluation_profit = (
            evaluation_amount - remaining_buy_amount
        )

        if remaining_buy_amount == 0:
            profit_rate = Decimal("0")
        else:
            profit_rate = (
                evaluation_profit / remaining_buy_amount
            ) * Decimal("100")

        buy_trades.append({
            "uuid": row[1],
            "created_at": row[12],
            "buy_price": float(buy_price),
            "quantity": float(remaining_quantity),
            "buy_amount": float(remaining_buy_amount),
            "fee_amount": float(remaining_fee_amount),
            "total_buy_amount": float(
                remaining_buy_amount
                + remaining_fee_amount
            ),
            "evaluation_amount": float(evaluation_amount),
            "evaluation_profit": float(evaluation_profit),
            "profit_rate": float(profit_rate),
        })

    return {
        "market": result["market"],
        "coin_name": COIN_NAMES[market],
        "current_price": float(result["current_price"]),
        "quantity": float(result["quantity"]),
        "average_buy_price": float(
            result["average_buy_price"]
        ),
        "total_buy_amount": float(
            result["total_buy_amount"]
        ),
        "evaluation_amount": float(
            result["evaluation_amount"]
        ),
        "evaluation_profit": float(
            result["evaluation_profit"]
        ),
        "profit_rate": float(result["profit_rate"]),
        "buy_trades": buy_trades,
    }