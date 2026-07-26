from decimal import Decimal

import requests


BASE_URL = "https://api.upbit.com"


def get_current_prices(markets: list[str]) -> dict[str, Decimal]:
    response = requests.get(
        f"{BASE_URL}/v1/ticker",
        params={
            "markets": ",".join(markets),
        },
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(response.json())

    prices = {}

    for ticker in response.json():
        market = ticker["market"]
        current_price = Decimal(str(ticker["trade_price"]))

        prices[market] = current_price

    return prices