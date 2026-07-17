import os
import uuid

import jwt
import requests
from dotenv import load_dotenv

from decimal import Decimal


load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

BASE_URL = "https://api.upbit.com"
PATH = "/v1/accounts"

def create_headers():
    payload = {
        "access_key": ACCESS_KEY,
        "nonce": str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, SECRET_KEY)

    return {
        "Authorization": f"Bearer {jwt_token}",
    }

def get_account_assets():
    response = requests.get(
        BASE_URL + PATH,
        headers=create_headers(),
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(response.json())

    accounts = response.json()

    assets = {}

    for account in accounts:
        currency = account["currency"]

        if currency == "KRW":
            continue

        balance = Decimal(account["balance"])
        locked = Decimal(account["locked"])
        avg_buy_price = Decimal(account["avg_buy_price"])

        quantity = balance + locked

        # 현재 보유수량이 없는 코인은 제외
        if quantity <= 0:
            continue

        assets[f"KRW-{currency}"] = {
            "quantity": quantity,
            "average_buy_price": avg_buy_price,
        }

    return assets