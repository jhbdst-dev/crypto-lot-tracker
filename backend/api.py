from fastapi import FastAPI

from backend.calculator import (
    calculate_coin_asset,
    calculate_home_summary,
)

from backend.upbit_accounts import get_account_assets
from backend.upbit_prices import get_current_prices

from fastapi.middleware.cors import CORSMiddleware

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