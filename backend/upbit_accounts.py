import os
import uuid
from decimal import Decimal

import jwt
import requests
from dotenv import load_dotenv

# .env 파일의 환경변수 로드
load_dotenv()

# 업비트 API 인증 정보
ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

# 업비트 계좌 조회 API 주소
BASE_URL = "https://api.upbit.com"
PATH = "/v1/accounts"

# 업비트 API 인증 헤더 생성
def create_headers():

    # JWT에 포함될 인증 정보 생성
    payload = {
        "access_key": ACCESS_KEY,
        "nonce": str(uuid.uuid4()),
    }

    # JWT 토큰 생성
    jwt_token = jwt.encode(payload, SECRET_KEY)

    # Authorization 헤더 반환
    return {
        "Authorization": f"Bearer {jwt_token}",
    }

# 업비트 계좌의 현재 보유자산 조회
def get_account_assets():

    # 업비트 계좌 조회 API 요청
    response = requests.get(
        BASE_URL + PATH,
        headers=create_headers(),
        timeout=10,
    )

    # 요청 실패 시 예외 발생
    if response.status_code != 200:
        raise RuntimeError(response.json())

    # API 응답(JSON) 가져오기
    accounts = response.json()

    # 현재 보유자산 저장
    assets = {}

    # 계좌 정보를 하나씩 확인
    for account in accounts:

        # 코인 심볼 추출
        currency = account["currency"]

        # 원화(KRW)는 제외
        if currency == "KRW":
            continue

        # 보유수량, 주문 중 수량, 평균 매수가 추출
        balance = Decimal(account["balance"])
        locked = Decimal(account["locked"])
        avg_buy_price = Decimal(account["avg_buy_price"])

        # 실제 보유수량 계산
        # 사용 가능 수량 + 주문 중 수량
        quantity = balance + locked

        # 현재 보유수량이 없는 코인은 제외
        if quantity <= 0:
            continue

        # 코인별 보유정보 저장
        assets[f"KRW-{currency}"] = {
            "quantity": quantity,
            "average_buy_price": avg_buy_price,
        }

    # 현재 보유자산 반환
    return assets