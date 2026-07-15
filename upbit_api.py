import hashlib
import os
import uuid
from urllib.parse import urlencode, unquote

import jwt
import requests
from dotenv import load_dotenv

from database import save_trades, get_last_trade_time
from datetime import datetime, timedelta, timezone

load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

BASE_URL = "https://api.upbit.com"
PATH = "/v1/orders/closed"

KST = timezone(timedelta(hours=9))
now = datetime.now(KST)

last_trade_time = get_last_trade_time()

if last_trade_time is None:
    start_time = datetime(
        year=2021,
        month=1,
        day=1,
        tzinfo=KST,
    )
else:
    start_time = last_trade_time

while start_time < now:
    # 최대 조회 범위인 7일 뒤를 종료 시간으로 설정
    end_time = min(
        start_time + timedelta(days=7),
        now,
    )

    params = {
        "state": "done",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "limit": 100,
    }

    query_string = unquote(urlencode(params))

    query_hash = hashlib.sha512(
        query_string.encode("utf-8")
    ).hexdigest()

    payload = {
        "access_key": ACCESS_KEY,
        "nonce": str(uuid.uuid4()),
        "query_hash": query_hash,
        "query_hash_alg": "SHA512",
    }

    jwt_token = jwt.encode(payload, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {jwt_token}",
    }

    response = requests.get(
        BASE_URL + PATH,
        params=params,
        headers=headers,
        timeout=10,
    )

    print(
        f"조회 기간: {start_time.isoformat()} "
        f"~ {end_time.isoformat()}"
    )
    print("상태 코드:", response.status_code)

    if response.status_code != 200:
        print("API 오류:", response.json())
        break

    trades = response.json()
    save_trades(trades)

    print(f"{len(trades)}건 조회 및 저장 시도")

    # 다음 조회는 이번 종료 시점부터 시작
    start_time = end_time