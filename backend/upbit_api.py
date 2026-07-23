# 파이썬 기본 모듈
import hashlib
import os
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, unquote

# 외부 라이브러리
import jwt
import requests
from dotenv import load_dotenv

# 프로젝트 내부 모듈
from backend.database import save_trades, get_last_trade_time

# .env 파일의 환경변수 로드
load_dotenv()

# 업비트 API 인증 정보
ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

# 업비트 종료 주문 조회 API 주소
BASE_URL = "https://api.upbit.com"
PATH = "/v1/orders/closed"

# 한국 시간대 설정
KST = timezone(timedelta(hours=9))

# 현재 한국 시간
now = datetime.now(KST)

# DB에 저장된 가장 최근 거래 시간 조회
last_trade_time = get_last_trade_time()

# 저장된 거래가 없으면 2021년부터 조회
if last_trade_time is None:
    start_time = datetime(
        year=2021,
        month=1,
        day=1,
        tzinfo=KST,
    )

# 저장된 거래가 있으면 최근 거래 시간부터 조회
else:
    start_time = last_trade_time

# 시작 시간부터 현재까지 거래내역을 7일 단위로 반복 조회
while start_time < now:
    
    # 업비트 API 최대 조회 범위에 맞춰 종료 시간 설정
    # 최대 조회 범위인 7일 뒤를 종료 시간으로 설정
    end_time = min(
        start_time + timedelta(days=7),
        now,
    )

    # 거래내역 조회 조건 생성
    params = {
        "states[]": ["done", "cancel"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "limit": 1000,
    }

    # 조회 조건을 URL 쿼리 문자열로 변환
    query_string = unquote(
    urlencode(params, doseq=True)
    )

    # 조회 조건을 SHA-512 방식으로 암호화
    query_hash = hashlib.sha512(
        query_string.encode("utf-8")
    ).hexdigest()

    # JWT에 포함할 인증 정보 생성
    payload = {
        "access_key": ACCESS_KEY,
        "nonce": str(uuid.uuid4()),
        "query_hash": query_hash,
        "query_hash_alg": "SHA512",
    }

    # JWT 인증 토큰 생성
    jwt_token = jwt.encode(payload, SECRET_KEY)

    # API 요청 인증 헤더 생성
    headers = {
        "Authorization": f"Bearer {jwt_token}",
    }

    # 업비트 종료 주문내역 조회 요청
    response = requests.get(
        BASE_URL + PATH,
        params=params,
        headers=headers,
        timeout=10,
    )

    # API 요청 실패 시 오류를 출력하고 조회 중단
    if response.status_code != 200:
        print("API 오류:", response.json())
        break

    # API 응답에서 거래내역 가져오기
    trades = response.json()

    # 조회한 거래내역을 DB에 저장
    save_trades(trades)

    # 다음 조회는 이번 종료 시점부터 시작
    start_time = end_time